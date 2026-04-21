"""
SIWES Models
Student Industrial Work Experience Scheme
"""
from django.db import models


class SiwesPlacement(models.Model):
    """SIWES placement"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    address = models.TextField()
    supervisor = models.CharField(max_length=255)
    supervisor_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    logbook_weekly = models.BooleanField(default=True)
    report_required = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )


class SiwesLog(models.Model):
    """Weekly logbook entry"""
    placement = models.ForeignKey(SiwesPlacement, on_delete=models.CASCADE, related_name='logs')
    week_number = models.IntegerField()
    date = models.DateField()
    activities = models.TextField()
    skills_acquired = models.JSONField(default=list)
    supervisor_remark = models.TextField(blank=True)
    approved = models.BooleanField(default=False)


class SiwesAssessment(models.Model):
    """SIWES assessment"""
    placement = models.ForeignKey(SiwesPlacement, on_delete=models.CASCADE)
    criteria = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)