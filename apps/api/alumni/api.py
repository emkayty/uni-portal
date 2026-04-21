"""
Alumni API
Alumni network and tracking
"""
from typing import Optional, List
from datetime import datetime

from django.db.models import Q, Count
from django.utils import timezone
from ninja import Router, Query

from .models import (
    AlumniProfile, AlumniEvent, Donation, JobPlacement,
    EmploymentStatus
)

router = Router()


# ============ ALUMNI PROFILE ENDPOINTS ============

@router.get("/profiles", response=List[dict])
def list_alumni(
    request,
    graduation_year: Optional[int] = Query(None),
    industry: Optional[str] = Query(None),
    employment_status: Optional[str] = Query(None)
):
    """List alumni profiles"""
    queryset = AlumniProfile.objects.filter(is_public=True)
    
    if graduation_year:
        queryset = queryset.filter(graduation_year=graduation_year)
    if industry:
        queryset = queryset.filter(industry=industry)
    if employment_status:
        queryset = queryset.filter(employment_status=employment_status)
    
    return [{
        'id': str(a.id),
        'matric_number': a.student.matric_number,
        'name': str(a.student.user.name) if a.student.user else None,
        'graduation_year': a.graduation_year,
        'employment_status': a.employment_status,
        'current_employer': a.current_employer,
        'job_title': a.job_title,
        'industry': a.industry,
        'location': a.location,
        'linkedin': a.linkedin
    } for a in queryset[:50]]


@router.get("/profiles/{alumni_id}")
def get_alumni_profile(request, alumni_id: str):
    """Get alumni profile"""
    try:
        profile = AlumniProfile.objects.get(id=alumni_id)
        return {
            'id': str(profile.id),
            'matric_number': profile.student.matric_number,
            'name': str(profile.student.user.name) if profile.student.user else None,
            'graduation_year': profile.graduation_year,
            'degree_classification': profile.degree_classification,
            'employment_status': profile.employment_status,
            'current_employer': profile.current_employer,
            'job_title': profile.job_title,
            'industry': profile.industry,
            'location': profile.location,
            'bio': profile.bio,
            'linkedin': profile.linkedin,
            'twitter': profile.twitter,
            'annual_dues_paid': profile.annual_dues_paid,
            'job_history': [{
                'employer': j.employer,
                'job_title': j.job_title,
                'industry': j.industry,
                'start_date': j.start_date.isoformat() if j.start_date else None,
                'is_current': j.is_current
            } for j in profile.job_history.all()[:5]]
        }
    except AlumniProfile.DoesNotExist:
        return {'error': 'Alumni profile not found'}


@router.post("/profiles")
def create_alumni_profile(request, data: dict):
    """Convert student to alumni"""
    try:
        from students.models import Student
        
        student = Student.objects.get(id=data['student_id'])
        
        # Check if already alumni
        existing = AlumniProfile.objects.filter(student=student).first()
        if existing:
            return {'error': 'Already an alumni'}
        
        profile = AlumniProfile.objects.create(
            student=student,
            graduation_year=data['graduation_year'],
            convocation_year=data.get('convocation_year'),
            degree_classification=data.get('degree_classification', '')
        )
        
        return {
            'id': str(profile.id),
            'message': 'Alumni profile created'
        }
    except Exception as e:
        return {'error': str(e)}


@router.put("/profiles/{alumni_id}")
def update_alumni_profile(request, alumni_id: str, data: dict):
    """Update alumni profile"""
    try:
        profile = AlumniProfile.objects.get(id=alumni_id)
        
        profile.employment_status = data.get('employment_status', profile.employment_status)
        profile.current_employer = data.get('current_employer', profile.current_employer)
        profile.job_title = data.get('job_title', profile.job_title)
        profile.industry = data.get('industry', profile.industry)
        profile.location = data.get('location', profile.location)
        profile.phone = data.get('phone', profile.phone)
        profile.linkedin = data.get('linkedin', profile.linkedin)
        profile.twitter = data.get('twitter', profile.twitter)
        profile.bio = data.get('bio', profile.bio)
        profile.save()
        
        return {'message': 'Profile updated'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/profiles/{alumni_id}/employment")
def add_employment(request, alumni_id: str, data: dict):
    """Add employment to job history"""
    try:
        profile = AlumniProfile.objects.get(id=alumni_id)
        
        # Mark current as not current
        JobPlacement.objects.filter(
            alumni=profile,
            is_current=True
        ).update(is_current=False)
        
        job = JobPlacement.objects.create(
            alumni=profile,
            employer=data['employer'],
            job_title=data['job_title'],
            industry=data.get('industry', ''),
            location=data.get('location', ''),
            start_date=data['start_date'],
            salary_range=data.get('salary_range', ''),
            is_current=True
        )
        
        # Update current employer
        profile.current_employer = data['employer']
        profile.job_title = data['job_title']
        profile.save()
        
        return {'id': str(job.id), 'message': 'Employment added'}
    except Exception as e:
        return {'error': str(e)}


# ============ ALUMNI EVENTS ============

@router.get("/events", response=List[dict])
def list_alumni_events(request, event_type: Optional[str] = Query(None)):
    """List alumni events"""
    queryset = AlumniEvent.objects.filter(
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
def create_alumni_event(request, data: dict):
    """Create alumni event"""
    event = AlumniEvent.objects.create(
        university_id=data['university_id'],
        title=data['title'],
        description=data['description'],
        event_type=data.get('event_type', 'reunion'),
        event_date=data['event_date'],
        location=data.get('location', ''),
        is_virtual=data.get('is_virtual', False)
    )
    
    return {'id': str(event.id), 'message': 'Event created'}


# ============ DONATIONS ============

@router.get("/donations")
def list_donations(request, alumni_id: Optional[str] = Query(None)):
    """List donations"""
    queryset = Donation.objects.all()
    if alumni_id:
        queryset = queryset.filter(alumni_id=alumni_id)
    
    return [{
        'id': str(d.id),
        'amount': float(d.amount),
        'purpose': d.purpose,
        'is_anonymous': d.is_anonymous,
        'message': d.message,
        'created_at': d.created_at.isoformat() if d.created_at else None
    } for d in queryset[:50]]


@router.post("/donations")
def make_donation(request, data: dict):
    """Make a donation"""
    try:
        profile = AlumniProfile.objects.get(id=data['alumni_id'])
        
        donation = Donation.objects.create(
            alumni=profile,
            amount=data['amount'],
            purpose=data.get('purpose', 'general'),
            payment_method=data.get('payment_method', 'card'),
            transaction_ref=data['transaction_ref'],
            is_anonymous=data.get('is_anonymous', False),
            message=data.get('message', '')
        )
        
        return {
            'id': str(donation.id),
            'message': 'Thank you for your donation!'
        }
    except Exception as e:
        return {'error': str(e)}


@router.get("/donations/totals")
def get_donation_totals(request):
    """Get total donations"""
    total = Donation.objects.aggregate(total=Count('amount'))
    by_purpose = {}
    for purpose in ['scholarship', 'infrastructure', 'research', 'general']:
        amount = Donation.objects.filter(purpose=purpose).aggregate(
            total=Count('amount')
        )['total'] or 0
        by_purpose[purpose] = amount
    
    return {
        'total_donors': Donation.objects.values('alumni').distinct().count(),
        'total_amount': total['total'] or 0,
        'by_purpose': by_purpose
    }


# ============ STATISTICS ============

@router.get("/statistics")
def get_alumni_statistics(request):
    """Get alumni statistics"""
    total_alumni = AlumniProfile.objects.count()
    employed = AlumniProfile.objects.filter(
        employment_status__in=[EmploymentStatus.EMPLOYED, EmploymentStatus.SELF_EMPLOYED]
    ).count()
    entrepreneurs = AlumniProfile.objects.filter(
        employment_status=EmploymentStatus.ENTREPRENEUR
    ).count()
    further_study = AlumniProfile.objects.filter(
        employment_status=EmploymentStatus.FURTHER_STUDY
    ).count()
    verifications = AlumniProfile.objects.filter(is_verified=True).count()
    
    # By graduation year
    by_year = {}
    for year in range(2015, 2026):
        count = AlumniProfile.objects.filter(graduation_year=year).count()
        if count > 0:
            by_year[str(year)] = count
    
    # By industry
    by_industry = {}
    industries = AlumniProfile.objects.values('industry').distinct()
    for ind in industries:
        if ind['industry']:
            count = AlumniProfile.objects.filter(industry=ind['industry']).count()
            by_industry[ind['industry']] = count
    
    return {
        'total_alumni': total_alumni,
        'employed': employed,
        'entrepreneurs': entrepreneurs,
        'further_study': further_study,
        'verified': verifications,
        'by_year': by_year,
        'by_industry': by_industry
    }


@router.get("/search")
def search_alumni(request, query: str = ''):
    """Search alumni"""
    profiles = AlumniProfile.objects.filter(
        Q(student__matric_number__icontains=query) |
        Q(student__user__first_name__icontains=query) |
        Q(student__user__last_name__icontains=query) |
        Q(current_employer__icontains=query) |
        Q(job_title__icontains=query)
    )[:20]
    
    return [{
        'id': str(p.id),
        'name': str(p.student.user.name) if p.student.user else None,
        'matric_number': p.student.matric_number,
        'current_employer': p.current_employer,
        'job_title': p.job_title
    } for p in profiles]