"""
Student Models
Comprehensive student records with system-aware fields
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from decimal import Decimal


class User(AbstractBaseUser, PermissionsMixin):
    """Extended user model for university portal"""
    
    class UserType(models.TextChoices):
        STUDENT = 'student', 'Student'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Administrator'
    
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STUDENT)
    
    # Common fields
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    alternate_email = models.EmailField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # For Nigerian system
    jamb_registration_number = models.CharField(max_length=20, blank=True)
    caps_id = models.CharField(max_length=50, blank=True)
    
    # Biometrics
    biometric_id = models.CharField(max_length=100, blank=True)
    biometric_data = models.JSONField(null=True, blank=True)
    
    # Last login tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    # MFA
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=100, blank=True)
    
    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Student(models.Model):
    """Student model with system-aware fields"""
    
    class Status(models.TextChoices):
        PROSPECTIVE = 'prospective', 'Prospective'
        ADMITTED = 'admitted', 'Admitted'
        MATRICULATED = 'matriculated', 'Matriculated'
        ACTIVE = 'active', 'Active'
        GRADUATING = 'graduating', 'Graduating'
        GRADUATED = 'graduated', 'Graduated'
        SUSPENDED = 'suspended', 'Suspended'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # University
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='students')
    
    # Programme
    programme = models.ForeignKey('university.Programme', on_delete=models.CASCADE, related_name='students')
    level = models.IntegerField(default=100)  # 100, 200, 300, 400, 500 (for medical)
    
    # Student ID
    student_id = models.CharField(max_length=20, unique=True)  # University specific ID
    
    # JAMB details (Nigerian)
    jamb_registration_number = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    post_utme_score = models.IntegerField(null=True, blank=True)
    admission_method = models.CharField(max_length=50, blank=True)  # UTME, DE, etc.
    
    # Matriculation
    matriculation_number = models.CharField(max_length=30, blank=True)
    matriculation_date = models.DateField(null=True, blank=True)
    
    # Personal details
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    genotype = models.CharField(max_length=5, blank=True)
    
    # Contact
    address = models.TextField(blank=True)
    state_of_origin = models.CharField(max_length=50, blank=True)
    lga = models.CharField(max_length=50, blank=True)
    
    # Next of kin
    next_of_kin_name = models.CharField(max_length=100, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)
    next_of_kin_relationship = models.CharField(max_length=50, blank=True)
    next_of_kin_address = models.TextField(blank=True)
    
    # Academic status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROSPECTIVE)
    
    # American specific
    student_type = models.CharField(max_length=20, blank=True)  # Freshman, Transfer
    gpa_scale = models.FloatField(default=4.0)
    total_credits = models.IntegerField(default=0)
    majors = models.JSONField(default=list)
    minors = models.JSONField(default=list)
    
    # Nigerian specific
    siwes_completed = models.BooleanField(default=False)
    siwes_year = models.IntegerField(null=True, blank=True)
    
    # Hostel
    hostel_assigned = models.ForeignKey('academic.Hostel', null=True, blank=True, on_delete=models.SET_NULL)
    room_number = models.CharField(max_length=20, blank=True)
    
    # Clearance
    departmental_clearance = models.BooleanField(default=False)
    library_clearance = models.BooleanField(default=False)
    hostel_clearance = models.BooleanField(default=False)
    finance_clearance = models.BooleanField(default=False)
    medical_clearance = models.BooleanField(default=False)
    final_clearance = models.BooleanField(default=False)
    
    # Academic standing
    on_probation = models.BooleanField(default=False)
    probation_reason = models.TextField(blank=True)
    outstanding_deficits = models.IntegerField(default=0)
    
    # Timestamps
    admitted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'students'
        unique_together = ['university', 'student_id']
        ordering = ['-admitted_at']
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
    
    def calculate_gpa(self):
        """Calculate current GPA based on system"""
        from django.db.models import Avg, Sum
        from decimal import Decimal
        
        results = self.enrollment_results.filter(approved=True)
        if not results.exists():
            return Decimal('0.0')
        
        total_points = Decimal('0.0')
        total_units = 0
        
        university = self.university
        grading = university.get_grading_config()
        
        for result in results:
            course = result.course
            score = result.total_score
            
            # Find grade
            grade = 'F'
            points = 0
            for g, config in grading.items():
                if config['min'] <= score <= config['max']:
                    grade = g
                    points = config['points']
                    break
            
            if university.academic_system == 'polytechnic':
                total_points += Decimal(str(points * course.credit_units))
                total_units += course.credit_units
            else:
                total_points += Decimal(str(points * course.units))
                total_units += course.units
        
        if total_units == 0:
            return Decimal('0.0')
        
        return total_points / total_units
    
    def get_classification(self):
        """Get degree classification based on system"""
        gpa = self.calculate_gpa()
        university = self.university
        
        if university.academic_system == 'american':
            if gpa >= 3.9:
                return "President's List"
            elif gpa >= 3.5:
                return "Dean's List"
            elif gpa >= 2.0:
                return "Good Standing"
            else:
                return "Academic Probation"
        
        # Nigerian system
        if gpa >= Decimal('4.5'):
            return "First Class"
        elif gpa >= Decimal('3.5'):
            return "Second Class Upper"
        elif gpa >= Decimal('2.5'):
            return "Second Class Lower"
        elif gpa >= Decimal('2.0'):
            return "Third Class"
        else:
            return "Pass"


class StudentDocuments(models.Model):
    """Student document storage"""
    
    class DocumentType(models.TextChoices):
        ADMISSION_LETTER = 'admission_letter', 'Admission Letter'
        JAMB_ADMISSION = 'jamb_admission', 'JAMB Admission'
        O_LEVEL_RESULT = 'o_level_result', 'O-Level Result'
        A_LEVEL_RESULT = 'a_level_result', 'A-Level Result'
        BIRTH_CERTIFICATE = 'birth_certificate', 'Birth Certificate'
        ID_CARD = 'id_card', 'ID Card'
        MEDICAL_REPORT = 'medical_report', 'Medical Report'
        SIWES_CERTIFICATE = 'siwes_certificate', 'SIWES Certificate'
        TRANSCRIPT = 'transcript', 'Transcript'
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    
    file = models.FileField(upload_to='student_documents/')
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'student_documents'


class StudentStatusHistory(models.Model):
    """Track student status changes"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='status_history')
    
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    reason = models.TextField()
    
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'student_status_history'
        ordering = ['-changed_at']