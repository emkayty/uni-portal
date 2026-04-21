"""
Alumni Models
Alumni network and tracking
"""
from django.db import models
from django.conf import settings


class EmploymentStatus(models.TextChoices):
    EMPLOYED = 'employed', 'Employed'
    SELF_EMPLOYED = 'self_employed', 'Self Employed'
    UNEMPLOYED = 'unemployed', 'Unemployed'
    FURTHER_STUDY = 'further_study', 'Further Study'
    ENTREPRENEUR = 'entrepreneur', 'Entrepreneur'


class AlumniProfile(models.Model):
    """Alumni profile (extends Student)"""
    student = models.OneToOneField(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='alumni_profile'
    )
    
    # Graduation details
    graduation_year = models.IntegerField()
    convocation_year = models.IntegerField(null=True, blank=True)
    degree_classification = models.CharField(max_length=50, blank=True)
    
    # Employment
    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED
    )
    current_employer = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    salary_range = models.CharField(max_length=50, blank=True)
    
    # Contact
    phone = models.CharField(max_length=50, blank=True)
    linkedin = models.URLField(max_length=500, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    
    # Profile
    bio = models.TextField(blank=True)
    profile_image = models.URLField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    # Dues
    annual_dues_paid = models.BooleanField(default=False)
    last_dues_year = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'alumni_profiles'
        ordering = ['-graduation_year']

    def __str__(self):
        return f"{self.student.matric_number} - Alumni"


class AlumniEvent(models.Model):
    """Alumni events"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='alumni_events'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('convocation', 'Convocation'),
            ('reunion', 'Reunion'),
            ('networking', 'Networking'),
            ('donation', 'Donation'),
            ('meeting', 'General Meeting')
        ]
    )
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    is_virtual = models.BooleanField(default=False)
    registration_link = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alumni_events'
        ordering = ['event_date']

    def __str__(self):
        return self.title


class Donation(models.Model):
    """Alumni donations"""
    alumni = models.ForeignKey(
        AlumniProfile,
        on_delete=models.CASCADE,
        related_name='donations'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='NGN')
    purpose = models.CharField(
        max_length=50,
        choices=[
            ('scholarship', 'Scholarship'),
            ('infrastructure', 'Infrastructure'),
            ('research', 'Research'),
            ('general', 'General')
        ]
    )
    payment_method = models.CharField(max_length=50)
    transaction_ref = models.CharField(max_length=100, unique=True)
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alumni_donations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alumni.student.matric_number} - {self.amount}"


class JobPlacement(models.Model):
    """Track alumni employment"""
    alumni = models.ForeignKey(
        AlumniProfile,
        on_delete=models.CASCADE,
        related_name='job_history'
    )
    employer = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    salary_range = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'alumni_job_placements'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.alumni.student.matric_number} - {self.job_title}"