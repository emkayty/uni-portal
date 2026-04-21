"""
Grade Appeal API
Student grade appeal workflow
"""
from typing import Optional, List
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query

from .models import (
    GradeAppeal, AppealEvidence, AppealComment, AppealTimeline,
    AppealStatus, AppealReason, GradeReviewCommittee
)

router = Router()


# ============ APPEAL ENDPOINTS ============

@router.get("/appeals", response=List[dict])
def list_appeals(
    request,
    status: Optional[str] = Query(None),
    student_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None)
):
    """List all grade appeals"""
    queryset = GradeAppeal.objects.all()
    
    if status:
        queryset = queryset.filter(status=status)
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    
    return [{
        'id': str(a.id),
        'student': a.student.matric_number,
        'course': a.course.code,
        'reason': a.reason,
        'status': a.status,
        'expected_grade': a.expected_grade,
        'actual_grade': a.actual_grade,
        'resolved_grade': a.resolved_grade,
        'created_at': a.created_at.isoformat() if a.created_at else None,
        'deadline': a.deadline.isoformat() if a.deadline else None
    } for a in queryset]


@router.get("/appeals/{appeal_id}")
def get_appeal(request, appeal_id: str):
    """Get appeal details"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        return {
            'id': str(appeal.id),
            'student': appeal.student.matric_number,
            'student_name': str(appeal.student.user.name) if appeal.student.user else None,
            'course': appeal.course.code,
            'course_name': appeal.course.title,
            'reason': appeal.reason,
            'description': appeal.description,
            'expected_grade': appeal.expected_grade,
            'actual_grade': appeal.actual_grade,
            'status': appeal.status,
            'evidence': appeal.evidence_files,
            'review_notes': appeal.review_notes,
            'resolved_grade': appeal.resolved_grade,
            'resolution_notes': appeal.resolution_notes,
            'created_at': appeal.created_at.isoformat() if appeal.created_at else None,
            'deadline': appeal.deadline.isoformat() if appeal.deadline else None,
            'comments': [{
                'user': c.user.username,
                'content': c.content,
                'is_internal': c.is_internal,
                'created_at': c.created_at.isoformat()
            } for c in appeal.comments.all()]
        }
    except GradeAppeal.DoesNotExist:
        return {'error': 'Appeal not found'}


@router.post("/appeals")
def create_appeal(request, data: dict):
    """Create a new grade appeal"""
    try:
        from academic.models import Enrollment
        from students.models import Student
        from academic.models import Course
        
        # Get enrollment
        enrollment = Enrollment.objects.get(id=data['enrollment_id'])
        student = Student.objects.get(id=data['student_id'])
        course = Course.objects.get(id=data['course_id'])
        
        # Check if appeal already exists
        existing = GradeAppeal.objects.filter(
            enrollment=enrollment,
            course=course
        ).first()
        
        if existing:
            return {'error': 'Appeal already exists for this course'}
        
        # Set deadline (14 days from now)
        deadline = timezone.now() + timedelta(days=14)
        
        appeal = GradeAppeal.objects.create(
            enrollment=enrollment,
            student=student,
            course=course,
            reason=data['reason'],
            description=data['description'],
            expected_grade=data.get('expected_grade', ''),
            actual_grade=data.get('actual_grade', ''),
            evidence_files=data.get('evidence', []),
            deadline=deadline
        )
        
        # Add to timeline
        AppealTimeline.objects.create(
            appeal=appeal,
            from_status='',
            to_status='pending'
        )
        
        return {
            'id': str(appeal.id),
            'message': 'Appeal submitted successfully',
            'deadline': deadline.isoformat()
        }
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/evidence")
def add_evidence(request, appeal_id: str, data: dict):
    """Add evidence to appeal"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        evidence = AppealEvidence.objects.create(
            appeal=appeal,
            file_name=data['file_name'],
            file_url=data['file_url'],
            file_type=data.get('file_type', 'document'),
            file_size=data.get('file_size', 0)
        )
        
        # Update appeal evidence list
        appeal.evidence_files.append(str(evidence.id))
        appeal.save()
        
        return {'id': str(evidence.id), 'message': 'Evidence added'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/comment")
def add_comment(request, appeal_id: str, data: dict):
    """Add comment to appeal"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        comment = AppealComment.objects.create(
            appeal=appeal,
            user_id=data['user_id'],
            content=data['content'],
            is_internal=data.get('is_internal', False)
        )
        return {'id': str(comment.id), 'message': 'Comment added'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/assign")
def assign_appeal(request, appeal_id: str, data: dict):
    """Assign appeal to reviewer"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        appeal.assigned_to_id = data['user_id']
        appeal.status = AppealStatus.UNDER_REVIEW
        appeal.save()
        
        # Add to timeline
        AppealTimeline.objects.create(
            appeal=appeal,
            from_status=appeal.status,
            to_status=AppealStatus.UNDER_REVIEW,
            changed_by_id=data.get('user_id')
        )
        
        return {'message': 'Appeal assigned'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/request-info")
def request_additional_info(request, appeal_id: str, data: dict):
    """Request additional information"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        old_status = appeal.status
        appeal.status = AppealStatus.ADDITIONAL_INFO
        appeal.review_notes = data.get('notes', '')
        appeal.save()
        
        AppealTimeline.objects.create(
            appeal=appeal,
            from_status=old_status,
            to_status=AppealStatus.ADDITIONAL_INFO,
            notes=data.get('notes', '')
        )
        
        return {'message': 'Information requested'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/approve")
def approve_appeal(request, appeal_id: str, data: dict):
    """Approve appeal and update grade"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        old_status = appeal.status
        
        appeal.status = AppealStatus.APPROVED
        appeal.resolved_grade = data.get('resolved_grade', '')
        appeal.resolution_notes = data.get('resolution_notes', '')
        appeal.reviewed_at = timezone.now()
        appeal.save()
        
        # Update timeline
        AppealTimeline.objects.create(
            appeal=appeal,
            from_status=old_status,
            to_status=AppealStatus.APPROVED,
            changed_by_id=data.get('user_id'),
            notes=data.get('resolution_notes', '')
        )
        
        # TODO: Update actual grade in enrollment
        # enrollment = appeal.enrollment
        # enrollment.grade = data.get('resolved_grade')
        # enrollment.save()
        
        return {'message': 'Appeal approved'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/reject")
def reject_appeal(request, appeal_id: str, data: dict):
    """Reject appeal"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        old_status = appeal.status
        
        appeal.status = AppealStatus.REJECTED
        appeal.review_notes = data.get('reason', '')
        appeal.resolution_notes = data.get('resolution_notes', '')
        appeal.reviewed_at = timezone.now()
        appeal.save()
        
        AppealTimeline.objects.create(
            appeal=appeal,
            from_status=old_status,
            to_status=AppealStatus.REJECTED,
            changed_by_id=data.get('user_id'),
            notes=data.get('resolution_notes', '')
        )
        
        return {'message': 'Appeal rejected'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/appeals/{appeal_id}/escalate")
def escalate_appeal(request, appeal_id: str, data: dict):
    """Escalate appeal to Senate"""
    try:
        appeal = GradeAppeal.objects.get(id=appeal_id)
        old_status = appeal.status
        
        appeal.status = AppealStatus.ESCALATED
        appeal.review_notes = data.get('reason', '')
        appeal.save()
        
        AppealTimeline.objects.create(
            appeal=appeal,
            from_status=old_status,
            to_status=AppealStatus.ESCALATED,
            notes=data.get('reason', '')
        )
        
        return {'message': 'Appeal escalated to Senate'}
    except Exception as e:
        return {'error': str(e)}


@router.get("/statistics")
def get_appeal_statistics(request):
    """Get appeal statistics"""
    total = GradeAppeal.objects.count()
    pending = GradeAppeal.objects.filter(status=AppealStatus.PENDING).count()
    under_review = GradeAppeal.objects.filter(status=AppealStatus.UNDER_REVIEW).count()
    approved = GradeAppeal.objects.filter(status=AppealStatus.APPROVED).count()
    rejected = GradeAppeal.objects.filter(status=AppealStatus.REJECTED).count()
    
    return {
        'total': total,
        'pending': pending,
        'under_review': under_review,
        'approved': approved,
        'rejected': rejected,
        'approval_rate': round(approved / total * 100, 2) if total > 0 else 0
    }


@router.get("/reasons")
def get_appeal_reasons(request):
    """Get available appeal reasons"""
    return [{'value': r.value, 'label': r.label} for r in AppealReason]