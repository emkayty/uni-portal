"""
Admission Models
JAMB CAPS integration, application processing
"""
import uuid
from django.db import models
from django.utils import timezone
from uuid import UUID


class AdmissionApplication(models.Model):
    """Admission application model"""
    
    class ApplicationStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        SCREENING = 'screening', 'Screening'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        OFFERED = 'offered', 'Offer Given'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='admission_applications')
    
    # Personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # JAMB Details
    jamb_registration_number = models.CharField(max_length=20)
    jamb_score = models.IntegerField()
    
    # For Nigerian
    jamb_subject_combination = models.JSONField(default=dict)
    
    # Application details
    first_choice_programme = models.ForeignKey('university.Programme', null=True, blank=True, on_delete=models.SET_NULL, related_name='first_choice_applications')
    second_choice_programme = models.ForeignKey('university.Programme', null=True, blank=True, on_delete=models.SET_NULL, related_name='second_choice_applications')
    
    # CAPS integration
    caps_application_id = models.CharField(max_length=50, blank=True)
    caps_status = models.CharField(max_length=50, blank=True)
    
    # Screening
    post_utme_score = models.IntegerField(null=True, blank=True)
    screening_aggregate = models.FloatField(null=True, blank=True)
    
    # Decision
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    
    # Offer
    offered_programme = models.ForeignKey('university.Programme', null=True, blank=True, on_delete=models.SET_NULL, related_name='offered_applications')
    offer_letter_sent = models.BooleanField(default=False)
    offer_accepted = models.BooleanField(default=False)
    
    # Admission
    admission_letter_number = models.CharField(max_length=30, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admission_applications'
        unique_together = ['university', 'jamb_registration_number']
    
    def __str__(self):
        return f"{self.jamb_registration_number} - {self.last_name}, {self.first_name}"


class CAPSDataImport(models.Model):
    """Track CAPS data imports"""
    
    class ImportStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='caps_imports')
    
    import_date = models.DateField()
    total_records = models.IntegerField(default=0)
    imported_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=ImportStatus.choices, default=ImportStatus.PENDING)
    
    error_log = models.TextField(blank=True)
    
    imported_by = models.ForeignKey('students.User', on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'caps_data_imports'
        ordering = ['-import_date']


class PostUTMEResult(models.Model):
    """Post-UTME screening results"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    application = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE, related_name='post_utme_results')
    
    score = models.IntegerField()
    max_score = models.IntegerField(default=100)
    percentile = models.FloatField(null=True, blank=True)
    
    # Subject scores
    subject_scores = models.JSONField(default=dict)
    
    is_passed = models.BooleanField(default=False)
    passing_score = models.IntegerField(default=50)
    
    exam_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_utme_results'


class AdmissionBatch(models.Model):
    """Admission batch management"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='admission_batches')
    
    name = models.CharField(max_length=100)  # e.g., 2024/2025 Session
    session = models.CharField(max_length=20)
    
    # Application period
    application_start = models.DateField()
    application_end = models.DateField()
    
    # Screening
    screening_start = models.DateField(null=True, blank=True)
    screening_end = models.DateField(null=True, blank=True)
    
    # Cut-off scores
    jamb_cutoff = models.IntegerField(default=160)
    post_utme_cutoff = models.IntegerField(default=50)
    
    # Capacity
    total_admission_quota = models.IntegerField()
    admitted_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'admission_batches'
        unique_together = ['university', 'session']


class DirectEntryApplication(models.Model):
    """Direct entry applications (for ND/HND holders)"""
    
    class ApplicationStatus(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        VERIFIED = 'verified', 'Verified'
        OFFERED = 'offered', 'Offer Given'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='de_applications')
    
    # Personal
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Previous qualification
    qualification = models.CharField(max_length=50)  # ND, HND, A-Level
    institution = models.CharField(max_length=200)
    graduation_year = models.IntegerField()
    cgpa = models.FloatField()
    
    # JAMB
    jamb_registration = models.CharField(max_length=20, blank=True)
    jamb_result = models.JSONField(default=dict)
    
    # Application
    programme = models.ForeignKey('university.Programme', on_delete=models.CASCADE, related_name='de_applications')
    
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.SUBMITTED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'direct_entry_applications'


class TransferApplication(models.Model):
    """Transfer applications from other universities"""
    
    class ApplicationStatus(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        TRANSCRIPT_VERIFIED = 'transcript_verified', 'Transcript Verified'
        SCREENING = 'screening', 'Screening'
        OFFERED = 'offered', 'Offer Given'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='transfer_applications')
    
    # Personal
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Current university
    current_institution = models.CharField(max_length=200)
    current_programme = models.CharField(max_length=200)
    current_level = models.IntegerField()
    current_cgpa = models.FloatField()
    
    # Application
    target_programme = models.ForeignKey('university.Programme', on_delete=models.CASCADE, related_name='transfer_applications')
    
    # Credits to transfer
    credits_to_transfer = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.SUBMITTED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'transfer_applications'


# Fix for TransferApplication UUID
from uuid import UUID