"""
Career Services API
Job placement and career services
"""
from typing import Optional, List
from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query

from .models import (
    Employer, Job, JobApplication, Interview, CareerEvent,
    JobType, JobStatus, ApplicationStatus
)

router = Router()


# ============ EMPLOYER ENDPOINTS ============

@router.get("/employers", response=List[dict])
def list_employers(request, industry: Optional[str] = Query(None)):
    """List employers"""
    queryset = Employer.objects.filter(is_active=True)
    if industry:
        queryset = queryset.filter(industry=industry)
    
    return [{
        'id': str(e.id),
        'name': e.name,
        'industry': e.industry,
        'website': e.website,
        'location': e.location,
        'is_verified': e.is_verified
    } for e in queryset]


@router.get("/employers/{employer_id}")
def get_employer(request, employer_id: str):
    """Get employer details"""
    try:
        employer = Employer.objects.get(id=employer_id)
        return {
            'id': str(employer.id),
            'name': employer.name,
            'industry': employer.industry,
            'website': employer.website,
            'description': employer.description,
            'location': employer.location,
            'contact_person': employer.contact_person,
            'contact_email': employer.contact_email,
            'is_verified': employer.is_verified,
            'jobs_count': employer.jobs.filter(status=JobStatus.ACTIVE).count()
        }
    except Employer.DoesNotExist:
        return {'error': 'Employer not found'}


@router.post("/employers")
def create_employer(request, data: dict):
    """Register employer"""
    employer = Employer.objects.create(
        name=data['name'],
        industry=data.get('industry', ''),
        website=data.get('website', ''),
        description=data.get('description', ''),
        location=data.get('location', ''),
        contact_person=data.get('contact_person', ''),
        contact_email=data.get('contact_email', ''),
        contact_phone=data.get('contact_phone', '')
    )
    return {'id': str(employer.id), 'message': 'Employer registered'}


# ============ JOB ENDPOINTS ============

@router.get("/jobs", response=List[dict])
def list_jobs(
    request,
    job_type: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    location: Optional[str] = Query(None)
):
    """List active jobs"""
    queryset = Job.objects.filter(status=JobStatus.ACTIVE)
    
    # Filter by deadline
    queryset = queryset.filter(Q(deadline__isnull=True) | Q(deadline__gte=timezone.now().date()))
    
    if job_type:
        queryset = queryset.filter(job_type=job_type)
    if location:
        queryset = queryset.filter(location__icontains=location)
    
    return [{
        'id': str(j.id),
        'title': j.title,
        'employer': j.employer.name,
        'job_type': j.job_type,
        'location': j.location,
        'salary': f"{j.salary_min}-{j.salary_max}" if j.salary_min else 'Competitive',
        'deadline': j.deadline.isoformat() if j.deadline else None,
        'posted_date': j.posted_date.isoformat() if j.posted_date else None
    } for j in queryset]


@router.get("/jobs/{job_id}")
def get_job(request, job_id: str):
    """Get job details"""
    try:
        job = Job.objects.get(id=job_id)
        
        # Increment views
        job.views += 1
        job.save(update_fields=['views'])
        
        return {
            'id': str(job.id),
            'title': job.title,
            'description': job.description,
            'requirements': job.requirements,
            'employer': {
                'id': str(job.employer.id),
                'name': job.employer.name,
                'industry': job.employer.industry,
                'website': job.employer.website
            },
            'job_type': job.job_type,
            'location': job.location,
            'salary': f"{job.salary_min}-{job.salary_max}" if job.salary_min else 'Competitive',
            'required_levels': job.required_levels,
            'skills_required': job.skills_required,
            'deadline': job.deadline.isoformat() if job.deadline else None,
            'views': job.views,
            'applications_count': job.applications.count()
        }
    except Job.DoesNotExist:
        return {'error': 'Job not found'}


@router.post("/jobs")
def create_job(request, data: dict):
    """Post a new job"""
    try:
        employer = Employer.objects.get(id=data['employer_id'])
        
        job = Job.objects.create(
            employer=employer,
            title=data['title'],
            description=data['description'],
            requirements=data.get('requirements', ''),
            job_type=data.get('job_type', JobType.FULL_TIME),
            location=data.get('location', ''),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            required_levels=data.get('required_levels', []),
            skills_required=data.get('skills_required', []),
            deadline=data.get('deadline'),
            start_date=data.get('start_date')
        )
        
        return {'id': str(job.id), 'message': 'Job posted'}
    except Exception as e:
        return {'error': str(e)}


# ============ APPLICATION ENDPOINTS ============

@router.post("/jobs/{job_id}/apply")
def apply_for_job(request, job_id: str, data: dict):
    """Apply for a job"""
    try:
        from students.models import Student
        
        job = Job.objects.get(id=job_id)
        student = Student.objects.get(id=data['student_id'])
        
        # Check if already applied
        existing = JobApplication.objects.filter(
            job=job,
            student=student
        ).first()
        
        if existing:
            return {'error': 'Already applied for this job'}
        
        application = JobApplication.objects.create(
            job=job,
            student=student,
            cover_letter=data.get('cover_letter', ''),
            resume_url=data.get('resume_url', '')
        )
        
        return {
            'id': str(application.id),
            'message': 'Application submitted'
        }
    except Exception as e:
        return {'error': str(e)}


@router.get("/applications", response=List[dict])
def list_applications(
    request,
    job_id: Optional[str] = Query(None),
    student_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List job applications"""
    queryset = JobApplication.objects.all()
    
    if job_id:
        queryset = queryset.filter(job_id=job_id)
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if status:
        queryset = queryset.filter(status=status)
    
    return [{
        'id': str(a.id),
        'job': a.job.title,
        'student': a.student.matric_number,
        'status': a.status,
        'applied_at': a.applied_at.isoformat() if a.applied_at else None
    } for a in queryset]


@router.post("/applications/{application_id}/update")
def update_application_status(request, application_id: str, data: dict):
    """Update application status"""
    try:
        application = JobApplication.objects.get(id=application_id)
        old_status = application.status
        
        application.status = data['status']
        application.notes = data.get('notes', '')
        application.save()
        
        return {'message': 'Status updated'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/applications/{application_id}/schedule")
def schedule_interview(request, application_id: str, data: dict):
    """Schedule interview"""
    try:
        application = JobApplication.objects.get(id=application_id)
        
        interview = Interview.objects.create(
            application=application,
            scheduled_date=data['scheduled_date'],
            location=data.get('location', ''),
            meeting_link=data.get('meeting_link', ''),
            notes=data.get('notes', '')
        )
        
        # Update status
        application.status = ApplicationStatus.INTERVIEW
        application.interview_date = data['scheduled_date']
        application.save()
        
        return {'id': str(interview.id), 'message': 'Interview scheduled'}
    except Exception as e:
        return {'error': str(e)}


# ============ CAREER EVENTS ============

@router.get("/events", response=List[dict])
def list_career_events(request, event_type: Optional[str] = Query(None)):
    """List career events"""
    queryset = CareerEvent.objects.filter(
        event_date__gte=timezone.now()
    )
    
    if event_type:
        queryset = queryset.filter(event_type=event_type)
    
    return [{
        'id': str(e.id),
        'title': e.title,
        'description': e.description,
        'event_type': e.event_type,
        'event_date': e.event_date.isoformat() if e.event_date else None,
        'location': e.location,
        'is_virtual': e.is_virtual
    } for e in queryset]


@router.post("/events")
def create_career_event(request, data: dict):
    """Create career event"""
    event = CareerEvent.objects.create(
        university_id=data['university_id'],
        title=data['title'],
        description=data['description'],
        event_type=data.get('event_type', 'workshop'),
        event_date=data['event_date'],
        location=data.get('location', ''),
        is_virtual=data.get('is_virtual', False)
    )
    
    return {'id': str(event.id), 'message': 'Event created'}


# ============ STATISTICS ============

@router.get("/statistics")
def get_career_statistics(request):
    """Get career statistics"""
    total_jobs = Job.objects.filter(status=JobStatus.ACTIVE).count()
    total_applications = JobApplication.objects.count()
    total_employers = Employer.objects.filter(is_active=True).count()
    
    # Application status breakdown
    by_status = {}
    for status in ApplicationStatus:
        count = JobApplication.objects.filter(status=status.value).count()
        by_status[status.value] = count
    
    # Recent placements
    recent_placements = JobApplication.objects.filter(
        status=ApplicationStatus.ACCEPTED,
        updated_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    return {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_employers': total_employers,
        'by_status': by_status,
        'recent_placements': recent_placements
    }


@router.get("/dashboard/{student_id}")
def get_student_dashboard(request, student_id: str):
    """Get student career dashboard"""
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    
    applications = JobApplication.objects.filter(student=student)
    
    return {
        'total_applications': applications.count(),
        'pending': applications.filter(status=ApplicationStatus.APPLIED).count(),
        'interviews': applications.filter(status=ApplicationStatus.INTERVIEW).count(),
        'rejected': applications.filter(status=ApplicationStatus.REJECTED).count(),
        'offered': applications.filter(status=ApplicationStatus.OFFERED).count()
    }