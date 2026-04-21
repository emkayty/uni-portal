"""
Exam Venue API
Exam venue and seating management
"""
from typing import Optional
from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query
from .models import Venue, ExamSeat, ExamAllocation

router = Router()


@router.get("/venues", response=list)
def list_venues(request, university_id: str = ''):
    venues = Venue.objects.all()
    if university_id:
        venues = venues.filter(university_id=university_id)
    return [{'id': str(v.id), 'name': v.name, 'capacity': v.capacity, 'building': v.building} for v in venues]


@router.post("/venues")
def create_venue(request, data: dict):
    venue = Venue.objects.create(
        university_id=data['university_id'],
        name=data['name'],
        capacity=data['capacity'],
        building=data.get('building', ''),
        floor=data.get('floor', '')
    )
    # Create seats
    for row in ['A', 'B', 'C', 'D', 'E']:
        for seat_num in range(1, int(venue.capacity/5) + 1):
            ExamSeat.objects.create(venue=venue, row=row, seat_number=str(seat_num))
    return {'id': str(venue.id), 'seats_created': venue.capacity}


@router.get("/allocations", response=list)
def list_allocations(request, session_id: str = ''):
    allocs = ExamAllocation.objects.all()
    if session_id:
        allocs = allocs.filter(session_id=session_id)
    return [{'course': a.course.code, 'venue': a.venue.name, 'date': a.exam_date, 'time': a.start_time} for a in allocs]


@router.post("/allocate")
def allocate_exam(request, data: dict):
    alloc = ExamAllocation.objects.create(
        course_id=data['course_id'],
        session_id=data['session_id'],
        venue_id=data['venue_id'],
        exam_date=data['exam_date'],
        start_time=data['start_time'],
        duration_minutes=data.get('duration_minutes', 60)
    )
    return {'id': str(alloc.id)}


@router.get("/timetable")
def get_exam_timetable(request, student_id: str = ''):
    return {'message': 'Exam timetable endpoint'}