"""
SIWES API
Student Industrial Work Experience Scheme
"""
from typing import Optional
from django.utils import timezone
from ninja import Router, Query
from .models import SiwesPlacement, SiwesLog, SiwesAssessment

router = Router()


@router.get("/placements", response=list)
def list_placements(request, status: str = ''):
    placements = SiwesPlacement.objects.all()
    if status:
        placements = placements.filter(status=status)
    return [{'id': str(p.id), 'student': p.student.matric_number, 'company': p.company, 'status': p.status} for p in placements]


@router.post("/placements")
def create_placement(request, data: dict):
    placement = SiwesPlacement.objects.create(
        student_id=data['student_id'],
        company=data['company'],
        address=data.get('address', ''),
        supervisor=data.get('supervisor', ''),
        supervisor_email=data.get('supervisor_email', ''),
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    return {'id': str(placement.id)}


@router.post("/placements/{placement_id}/approve")
def approve_placement(request, placement_id: str):
    placement = SiwesPlacement.objects.get(id=placement_id)
    placement.status = 'approved'
    placement.save()
    return {'message': 'Placement approved'}


@router.get("/logs", response=list)
def get_logs(request, placement_id: str = ''):
    logs = SiwesLog.objects.all()
    if placement_id:
        logs = logs.filter(placement_id=placement_id)
    return [{'week': l.week_number, 'activities': l.activities[:50]} for l in logs]


@router.post("/logs")
def create_log(request, data: dict):
    log = SiwesLog.objects.create(
        placement_id=data['placement_id'],
        week_number=data['week_number'],
        date=data['date'],
        activities=data['activities'],
        skills_acquired=data.get('skills', [])
    )
    return {'id': str(log.id)}


@router.get("/assessments")
def get_assessments(request, placement_id: str = ''):
    assessments = SiwesAssessment.objects.all()
    if placement_id:
        assessments = assessments.filter(placement_id=placement_id)
    return [{'criteria': a.criteria, 'score': float(a.score)} for a in assessments]