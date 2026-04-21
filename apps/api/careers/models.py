"""
Career Services Models
Job placement and career services
"""
from django.db import models
from django.conf import settings


class JobType(models.TextChoices):
    FULL_TIME = 'full_time', 'Full Time'
    PART_TIME = 'part_time', 'Part Time'
    CONTRACT = 'contract', 'Contract'
    INTERNSHIP = 'internship', 'Internship'
    SIWES = 'siwes', 'SIWES'
    VOLUNTEER = 'volunteer', 'Volunteer'


class JobStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    CLOSED = 'closed', 'Closed'
    EXPIRED = 'expired', 'Expired'


class ApplicationStatus(models.TextChoices):
    APPLIED = 'applied', 'Applied'
    SCREENING = 'screening', 'Screening'
    INTERVIEW = 'interview', 'Interview'
    SHORTLISTED = 'shortlisted', 'Shortlisted'
    REJECTED = 'rejected', 'Rejected'
    OFFERED = 'offered', 'Offered'
    ACCEPTED = 'accepted', 'Accepted'


class Employer(models.Model):
    """Employer/Company profile"""
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    website = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    logo = models.URLField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'career_employers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Job(models.Model):
    """Job posting"""
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices)
    location = models.CharField(max_length=255, blank=True)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='NGN')
    
    # Requirements
    required_levels = models.JSONField(default=list)  # List of year levels
    required_programs = models.JSONField(default=list)  # Programme codes
    skills_required = models.JSONField(default=list)
    
    # Dates
    posted_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.ACTIVE
    )
    views = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'career_jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.employer.name}"


class JobApplication(models.Model):
    """Job application"""
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    
    # Application details
    cover_letter = models.TextField(blank=True)
    resume_url = models.URLField(max_length=500, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED
    )
    
    # Review
    notes = models.TextField(blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(max_length=255, blank=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'career_applications'
        unique_together = ['job', 'student']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.matric_number} - {self.job.title}"


class Interview(models.Model):
    """Interview schedule"""
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    meeting_link = models.URLField(max_length=500, blank=True)
    notes = models.TextField(blank=True)
    result = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('passed', 'Passed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'career_interviews'
        ordering = ['scheduled_date']

    def __str__(self):
        return f"Interview - {self.application.job.title}"


class CareerEvent(models.Model):
    """Career fair, workshop events"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='career_events'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('career_fair', 'Career Fair'),
            ('workshop', 'Workshop'),
            ('seminar', 'Seminar'),
            ('networking', 'Networking')
        ]
    )
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    registration_link = models.URLField(max_length=500, blank=True)
    is_virtual = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'career_events'
        ordering = ['event_date']

    def __str__(self):
        return self.title


class Industry(models.Model):
    """Industry categories"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'career_industries'
        ordering = ['name']

    def __str__(self):
        return self.name