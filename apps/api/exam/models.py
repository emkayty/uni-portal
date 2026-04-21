"""
Exam Venue Models
Exam venue and seating management
"""
from django.db import models


class Venue(models.Model):
    """Exam venue/hall"""
    university = models.ForeignKey('university.University', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    is_accessible = models.BooleanField(default=True)


class ExamSeat(models.Model):
    """Seat assignment"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)
    is_accessible = models.BooleanField(default=False)


class ExamAllocation(models.Model):
    """Course exam allocation"""
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    session = models.ForeignKey('university.Session', on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    exam_date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    invigilators = models.JSONField(default=list)
    total_students = models.IntegerField(default=0)