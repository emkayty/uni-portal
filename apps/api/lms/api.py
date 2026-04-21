"""
LMS (Learning Management System) API
Blackboard, Canvas, Moodle integration
"""
import hashlib
import hmac
import json
import requests
from datetime import datetime
from typing import Optional, List

from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query

from .models import (
    LMSInstance, CourseMapping, ContentItem, VideoRecording,
    EnrollmentSync, GradeSync, Announcement, LMSProvider
)

router = Router()


# ============ LMS PROVIDER CLIENTS ============

class LMSClient:
    """Base client for LMS integration"""
    
    def __init__(self, instance: LMSInstance):
        self.instance = instance
        self.base_url = instance.base_url
        self.api_key = instance.api_key
        self.client_id = instance.client_id
        
    def test_connection(self) -> dict:
        """Test LMS connection"""
        raise NotImplementedError
    
    def sync_course(self, course_code: str, course_name: str) -> dict:
        """Create/sync course in LMS"""
        raise NotImplementedError
        
    def enroll_student(self, lms_course_id: str, student_id: str, email: str) -> dict:
        """Enroll student in LMS course"""
        raise NotImplementedError
        
    def push_grade(self, lms_course_id: str, student_id: str, score: float) -> dict:
        """Push grade to LMS"""
        raise NotImplementedError
        
    def get_content(self, lms_course_id: str) -> List[dict]:
        """Get course content from LMS"""
        raise NotImplementedError


class BlackboardClient(LMSClient):
    """Blackboard Learn client"""
    
    def test_connection(self) -> dict:
        """Test Blackboard API connection"""
        try:
            # Blackboard uses REST API with OAuth or API token
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(
                f"{self.base_url}/learn/api/public/v3/courses",
                headers=headers,
                timeout=10
            )
            return {
                'success': response.status_code == 200,
                'status': response.status_code,
                'message': 'Connected' if response.status_code == 200 else 'Failed'
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def sync_course(self, course_code: str, course_name: str) -> dict:
        """Create course in Blackboard"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'courseId': course_code,
                'name': course_name,
                'term': {'id': 'DEFAULT'}
            }
            response = requests.post(
                f"{self.base_url}/learn/api/public/v3/courses",
                headers=headers,
                json=data,
                timeout=30
            )
            return {
                'success': response.status_code in [200, 201],
                'lms_course_id': response.json().get('id', ''),
                'lms_course_url': f"{self.base_url}/webapps/blackboard/execute/"
                                 f"bbCourselinks?course_id={course_code}"
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}


class CanvasClient(LMSClient):
    """Canvas LMS client"""
    
    def test_connection(self) -> dict:
        """Test Canvas API connection"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(
                f"{self.base_url}/api/v1/users/self",
                headers=headers,
                timeout=10
            )
            return {
                'success': response.status_code == 200,
                'status': response.status_code,
                'message': 'Connected' if response.status_code == 200 else 'Failed'
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def sync_course(self, course_code: str, course_name: str) -> dict:
        """Create course in Canvas"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'course': {
                    'course_code': course_code,
                    'name': course_name,
                    'is_public': False
                }
            }
            response = requests.post(
                f"{self.base_url}/api/v1/accounts/self/courses",
                headers=headers,
                json=data,
                timeout=30
            )
            result = response.json()
            return {
                'success': response.status_code in [200, 201],
                'lms_course_id': str(result.get('id', '')),
                'lms_course_url': f"{self.base_url}/courses/{result.get('id')}"
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}


class MoodleClient(LMSClient):
    """Moodle client"""
    
    def test_connection(self) -> dict:
        """Test Moodle API connection"""
        try:
            params = {
                'wstoken': self.api_key,
                'wsfunction': 'core_webservice_get_site_info',
                'moodlewsrestformat': 'json'
            }
            response = requests.get(
                f"{self.base_url}/webservice/rest/server.php",
                params=params,
                timeout=10
            )
            return {
                'success': response.status_code == 200,
                'status': response.status_code,
                'message': 'Connected' if response.status_code == 200 else 'Failed'
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def sync_course(self, course_code: str, course_name: str) -> dict:
        """Create course in Moodle"""
        try:
            params = {
                'wstoken': self.api_key,
                'wsfunction': 'core_course_create_courses',
                'moodlewsrestformat': 'json',
                'courses[0][fullname]': course_name,
                'courses[0][shortname]': course_code,
                'courses[0][categoryid]': 1
            }
            response = requests.post(
                f"{self.base_url}/webservice/rest/server.php",
                data=params,
                timeout=30
            )
            result = response.json()
            return {
                'success': bool(result),
                'lms_course_id': str(result[0]['id']) if result else '',
                'lms_course_url': f"{self.base_url}/course/view.php?id={result[0]['id']}" if result else ''
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}


def get_lms_client(instance: LMSInstance) -> LMSClient:
    """Factory to get LMS client based on provider"""
    clients = {
        LMSProvider.BLACKBOARD: BlackboardClient,
        LMSProvider.CANVAS: CanvasClient,
        LMSProvider.MOODLE: MoodleClient
    }
    client_class = clients.get(instance.provider, BlackboardClient)
    return client_class(instance)


# ============ LMS INSTANCE ENDPOINTS ============

@router.get("/instances", response=List[dict])
def list_lms_instances(request, university_id: Optional[str] = Query(None)):
    """List all LMS instances"""
    queryset = LMSInstance.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return [{
        'id': str(lms.id),
        'university': lms.university.name,
        'provider': lms.provider,
        'base_url': lms.base_url,
        'is_active': lms.is_active,
        'created_at': lms.created_at.isoformat() if lms.created_at else None
    } for lms in queryset]


@router.post("/instances")
def create_lms_instance(request, data: dict):
    """Create LMS instance"""
    lms = LMSInstance.objects.create(
        university_id=data['university_id'],
        provider=data['provider'],
        base_url=data['base_url'],
        api_key=data.get('api_key', ''),
        api_secret=data.get('api_secret', ''),
        client_id=data.get('client_id', ''),
        is_active=data.get('is_active', True)
    )
    return {'id': str(lms.id), 'message': 'LMS instance created'}


@router.get("/instances/{instance_id}/test")
def test_lms_connection(request, instance_id: str):
    """Test LMS connection"""
    try:
        lms = LMSInstance.objects.get(id=instance_id)
        client = get_lms_client(lms)
        result = client.test_connection()
        return result
    except LMSInstance.DoesNotExist:
        return {'success': False, 'message': 'LMS instance not found'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@router.post("/instances/{instance_id}/sync-course")
def sync_course_to_lms(request, instance_id: str, course_id: str):
    """Sync a course to LMS"""
    try:
        from academic.models import Course
        lms = LMSInstance.objects.get(id=instance_id)
        course = Course.objects.get(id=course_id)
        
        # Check if mapping exists
        mapping, created = CourseMapping.objects.get_or_create(
            local_course=course,
            lms_instance=lms,
            defaults={'lms_course_id': ''}
        )
        
        client = get_lms_client(lms)
        result = client.sync_course(course.code, course.title)
        
        if result.get('success'):
            mapping.lms_course_id = result.get('lms_course_id', '')
            mapping.lms_course_url = result.get('lms_course_url', '')
            mapping.sync_status = 'synced'
            mapping.last_sync = timezone.now()
            mapping.save()
        else:
            mapping.sync_status = 'failed'
            mapping.save()
            
        return result
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ============ CONTENT MANAGEMENT ============

@router.get("/courses/{mapping_id}/content")
def get_course_content(request, mapping_id: str):
    """Get content for a course mapping"""
    try:
        mapping = CourseMapping.objects.get(id=mapping_id)
        items = mapping.content_items.all()
        
        return [{
            'id': str(item.id),
            'title': item.title,
            'content_type': item.content_type,
            'url': item.url,
            'file_size': item.file_size,
            'duration': item.duration,
            'is_published': item.is_published,
            'created_at': item.created_at.isoformat() if item.created_at else None
        } for item in items]
    except CourseMapping.DoesNotExist:
        return []


@router.post("/courses/{mapping_id}/content")
def add_content(request, mapping_id: str, data: dict):
    """Add content to course"""
    try:
        mapping = CourseMapping.objects.get(id=mapping_id)
        item = ContentItem.objects.create(
            course_mapping=mapping,
            lms_content_id=data.get('lms_content_id', ''),
            title=data['title'],
            content_type=data.get('content_type', 'file'),
            url=data.get('url', ''),
            file_size=data.get('file_size'),
            duration=data.get('duration'),
            is_published=data.get('is_published', False)
        )
        return {'id': str(item.id), 'message': 'Content added'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@router.post("/courses/{mapping_id}/content/{item_id}/video")
def add_video_content(request, mapping_id: str, item_id: str, data: dict):
    """Add video recording to content"""
    try:
        content = ContentItem.objects.get(id=item_id)
        video = VideoRecording.objects.create(
            content_item=content,
            video_url=data['video_url'],
            thumbnail_url=data.get('thumbnail_url', ''),
            duration_seconds=data['duration_seconds'],
            resolutions=data.get('resolutions', []),
            transcript=data.get('transcript', ''),
            subtitles=data.get('subtitles', {})
        )
        return {'id': str(video.id), 'message': 'Video added'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ============ ENROLLMENT SYNC ============

@router.post("/enrollments/sync")
def sync_enrollment_to_lms(request, data: dict):
    """Sync enrollment to LMS"""
    try:
        from academic.models import Enrollment
        enrollment = Enrollment.objects.get(id=data['enrollment_id'])
        lms = LMSInstance.objects.get(id=data['lms_instance_id'])
        
        # Get student info
        student = enrollment.student
        user = student.user
        
        client = get_lms_client(lms)
        result = client.enroll_student(
            data['lms_course_id'],
            str(user.id),
            user.email
        )
        
        if result.get('success'):
            EnrollmentSync.objects.update_or_create(
                enrollment=enrollment,
                lms_instance=lms,
                defaults={
                    'lms_user_id': str(user.id),
                    'lms_enrollment_id': result.get('enrollment_id', ''),
                    'status': 'enrolled'
                }
            )
        
        return result
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ============ GRADE SYNC ============

@router.post("/grades/sync")
def sync_grade_to_lms(request, data: dict):
    """Sync grade to LMS"""
    try:
        from academic.models import Enrollment
        enrollment = Enrollment.objects.get(id=data['enrollment_id'])
        lms = LMSInstance.objects.get(id=data['lms_instance_id'])
        
        client = get_lms_client(lms)
        result = client.push_grade(
            data['lms_course_id'],
            str(enrollment.student.user_id),
            float(data['score'])
        )
        
        if result.get('success'):
            GradeSync.objects.create(
                enrollment=enrollment,
                lms_instance=lms,
                lms_grade_id=result.get('grade_id', ''),
                score=data['score'],
                direction='to_lms'
            )
        
        return result
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ============ ANNOUNCEMENTS ============

@router.get("/announcements")
def list_announcements(request, course_id: Optional[str] = Query(None)):
    """List LMS announcements"""
    queryset = Announcement.objects.all()
    if course_id:
        queryset = queryset.filter(course_mapping_id=course_id)
    
    return [{
        'id': str(a.id),
        'title': a.title,
        'message': a.message,
        'is_published': a.is_published,
        'publish_date': a.publish_date.isoformat() if a.publish_date else None
    } for a in queryset]


@router.post("/announcements")
def create_announcement(request, data: dict):
    """Create LMS announcement"""
    announcement = Announcement.objects.create(
        course_mapping_id=data['course_mapping_id'],
        title=data['title'],
        message=data['message'],
        is_published=data.get('is_published', False),
        publish_date=data.get('publish_date')
    )
    return {'id': str(announcement.id), 'message': 'Announcement created'}


# ============ STATISTICS ============

@router.get("/statistics")
def get_lms_statistics(request, university_id: Optional[str] = Query(None)):
    """Get LMS statistics"""
    instances = LMSInstance.objects.all()
    if university_id:
        instances = instances.filter(university_id=university_id)
    
    total_instances = instances.count()
    active_instances = instances.filter(is_active=True).count()
    
    # Count mappings
    mappings = CourseMapping.objects.filter(lms_instance__in=instances)
    synced_courses = mappings.filter(sync_status='synced').count()
    pending_courses = mappings.filter(sync_status='pending').count()
    
    return {
        'total_instances': total_instances,
        'active_instances': active_instances,
        'total_courses': mappings.count(),
        'synced_courses': synced_courses,
        'pending_courses': pending_courses,
        'total_content_items': ContentItem.objects.filter(
            course_mapping__in=mappings
        ).count()
    }