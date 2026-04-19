"""
Core University Models
System-aware models supporting British/Nigerian and American university systems
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal


class AcademicSystem(models.TextChoices):
    """Academic system types"""
    BRITISH_NIGERIAN = 'british_nigerian', 'British/Nigerian (NUC)'
    AMERICAN = 'american', 'American (US Style)'
    POLYTECHNIC = 'polytechnic', 'Nigerian Polytechnic (NBTE)'


class SystemType(models.TextChoices):
    """Institution type"""
    UNIVERSITY = 'university', 'University'
    POLYTECHNIC = 'polytechnic', 'Polytechnic'


class ProgrammeType(models.TextChoices):
    """Programme types based on system"""
    # Nigerian University
    BACHELOR = 'bachelor', 'Bachelor Degree'
    MASTER = 'master', 'Master Degree'
    DOCTORATE = 'doctorate', 'Doctorate (PhD)'
    
    # Nigerian Polytechnic
    ND = 'nd', 'National Diploma (ND)'
    HND = 'hnd', 'Higher National Diploma (HND)'
    
    # American
    BSc = 'bsc', 'Bachelor of Science'
    BA = 'ba', 'Bachelor of Arts'
    MA = 'ma', 'Master of Arts'
    MS = 'ms', 'Master of Science'
    PhD = 'phd', 'Doctor of Philosophy'


class University(models.Model):
    """University/Institution model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, unique=True)  # JAMB code for Nigerian
    
    # System configuration
    academic_system = models.CharField(
        max_length=20,
        choices=AcademicSystem.choices,
        default=AcademicSystem.BRITISH_NIGERIAN
    )
    system_type = models.CharField(
        max_length=20,
        choices=SystemType.choices,
        default=SystemType.UNIVERSITY
    )
    
    # Regulatory
    nuc_accredited = models.BooleanField(default=True)
    nbte_accredited = models.BooleanField(default=False)  # For polytechnics
    tetfund_qualified = models.BooleanField(default=True)
    
    # Contact
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True)
    
    # Settings based on system
    sessions_per_year = models.IntegerField(default=2)
    max_courses_per_semester = models.IntegerField(default=6)
    min_courses_per_semester = models.IntegerField(default=4)
    
    # Grading scale reference
    grading_scale = models.CharField(max_length=50, default='default')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'universities'
    
    def __str__(self):
        return f"{self.short_name} - {self.name}"
    
    def get_grading_config(self):
        """Get grading configuration based on system"""
        if self.academic_system == AcademicSystem.BRITISH_NIGERIAN:
            return {
                'A': {'min': 70, 'max': 100, 'points': 5, 'desc': 'Excellent'},
                'B': {'min': 60, 'max': 69, 'points': 4, 'desc': 'Very Good'},
                'C': {'min': 50, 'max': 59, 'points': 3, 'desc': 'Good'},
                'D': {'min': 45, 'max': 49, 'points': 2, 'desc': 'Pass'},
                'E': {'min': 40, 'max': 44, 'points': 1, 'desc': 'Fair Pass'},
                'F': {'min': 0, 'max': 39, 'points': 0, 'desc': 'Fail'},
            }
        elif self.academic_system == AcademicSystem.POLYTECHNIC:
            return {
                'A': {'min': 80, 'max': 100, 'points': 4.0, 'desc': 'Excellent'},
                'AB': {'min': 75, 'max': 79, 'points': 3.5, 'desc': 'Very Good'},
                'B': {'min': 70, 'max': 74, 'points': 3.25, 'desc': 'Very Good'},
                'BC': {'min': 65, 'max': 69, 'points': 3.0, 'desc': 'Good'},
                'C': {'min': 60, 'max': 64, 'points': 2.75, 'desc': 'Good'},
                'CD': {'min': 55, 'max': 59, 'points': 2.5, 'desc': 'Credit'},
                'D': {'min': 50, 'max': 54, 'points': 2.25, 'desc': 'Credit'},
                'E': {'min': 45, 'max': 49, 'points': 2.0, 'desc': 'Pass'},
                'F': {'min': 0, 'max': 44, 'points': 0.0, 'desc': 'Fail'},
            }
        else:  # American
            return {
                'A+': {'min': 97, 'max': 100, 'points': 4.0},
                'A': {'min': 93, 'max': 96, 'points': 4.0},
                'A-': {'min': 90, 'max': 92, 'points': 3.7},
                'B+': {'min': 87, 'max': 89, 'points': 3.3},
                'B': {'min': 83, 'max': 86, 'points': 3.0},
                'B-': {'min': 80, 'max': 82, 'points': 2.7},
                'C+': {'min': 77, 'max': 79, 'points': 2.3},
                'C': {'min': 73, 'max': 76, 'points': 2.0},
                'C-': {'min': 70, 'max': 72, 'points': 1.7},
                'D+': {'min': 67, 'max': 69, 'points': 1.3},
                'D': {'min': 63, 'max': 66, 'points': 1.0},
                'D-': {'min': 60, 'max': 62, 'points': 0.7},
                'F': {'min': 0, 'max': 59, 'points': 0.0},
            }


class Faculty(models.Model):
    """Faculty/College model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)  # e.g., ENG, MED, LAW
    
    # Nigerian specific
    CCMAS_compliant = models.BooleanField(default=True)  # Core Curriculum
    
    dean = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'faculties'
        unique_together = ['university', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    """Department model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)  # e.g., CSE, MTH, PHY
    
    # Programme management
    programme_types = models.JSONField(default=list)  # List of programme types
    
    hod = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    
    # Accreditation
    nuc_accredited = models.BooleanField(default=True)
    accreditation_year = models.IntegerField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'departments'
        unique_together = ['faculty', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Programme(models.Model):
    """Programme/Degree model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programmes')
    
    name = models.CharField(max_length=200)  # e.g., Computer Science
    code = models.CharField(max_length=20)  # e.g., CSC
    
    # Programme characteristics
    programme_type = models.CharField(max_length=20, choices=ProgrammeType.choices)
    duration_years = models.IntegerField(default=4)
    
    # For Nigerian system
    CCMAS_code = models.CharField(max_length=20, blank=True)  # Benchmark code
    BMAS_code = models.CharField(max_length=20, blank=True)   # Minimum standards
    
    # For American system
    major = models.CharField(max_length=100, blank=True)
    minor = models.CharField(max_length=100, blank=True)
    liberal_arts = models.BooleanField(default=False)
    
    # Credit hours (American)
    required_credits = models.IntegerField(null=True, blank=True)
    general_education_credits = models.IntegerField(null=True, blank=True)
    
    # Admission
    UTME_subjects = models.JSONField(default=list)  # Required UTME subjects
    direct_entry_requirements = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'programmes'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Session(models.Model):
    """Academic session model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='sessions')
    
    session = models.CharField(max_length=20)  # e.g., 2024/2025
    is_current = models.BooleanField(default=False)
    
    # Session dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Registration periods
    registration_start = models.DateField(null=True, blank=True)
    registration_end = models.DateField(null=True, blank=True)
    
    # Fees (can be different per session)
    tuition_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_fees = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sessions'
        unique_together = ['university', 'session']
        ordering = ['-session']
    
    def __str__(self):
        return self.session


class Semester(models.Model):
    """Semester model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='semesters')
    
    name = models.CharField(max_length=20)  # First, Second, Third (for some)
    semester = models.IntegerField()  # 1, 2, 3
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Examination dates
    exam_start = models.DateField(null=True, blank=True)
    exam_end = models.DateField(null=True, blank=True)
    
    # Results
    results_released = models.BooleanField(default=False)
    results_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'semesters'
        unique_together = ['session', 'semester']
        ordering = ['semester']
    
    def __str__(self):
        return f"{self.session.session} - {self.name}"