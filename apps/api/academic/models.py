"""
Academic Models
Courses, grades, timetables - system aware for Nigerian/American systems
"""
import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal


class Course(models.Model):
    """Course model with system-aware structure"""
    
    class CourseType(models.TextChoices):
        CORE = 'core', 'Core/Elective'
        ELECTIVE = 'elective', 'Elective'
        GENERAL = 'general', 'General (GEC)'
        PROFESSIONAL = 'professional', 'Professional'
        VOCATIONAL = 'vocational', 'Vocational'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic info
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='courses')
    department = models.ForeignKey('university.Department', on_delete=models.CASCADE, related_name='courses')
    
    code = models.CharField(max_length=15)  # e.g., CSC101
    title = models.CharField(max_length=200)
    
    # Units/Credits
    units = models.IntegerField(default=3)  # Nigerian system
    credit_hours = models.IntegerField(default=3)  # American system
    
    # System-specific
    course_type = models.CharField(max_length=20, choices=CourseType.choices, default=CourseType.CORE)
    
    # For Nigerian system
    CCMAS_code = models.CharField(max_length=20, blank=True)  # Core Curriculum
    is_industrial_attachment = models.BooleanField(default=False)  # SIWES
    is_project = models.BooleanField(default=False)  # Final year project
    is_long_course = models.BooleanField(default=False)  # Courses over 2 semesters
    
    # Prerequisites
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    prerequisite_courses = models.JSONField(default=list)  # List of course codes
    
    # For American system
    is_general_education = models.BooleanField(default=False)
    distribution_area = models.CharField(max_length=50, blank=True)  # Humanities, Sciences, etc.
    
    # Level
    level = models.IntegerField(default=100)  # 100-500
    
    # Semester availability
    semester_offered = models.CharField(max_length=20, blank=True)  # First, Second, Both
    
    # Capacity
    max_capacity = models.IntegerField(default=500)
    current_enrollment = models.IntegerField(default=0)
    
    # Assessment weights (Nigerian)
    ca_weight = models.FloatField(default=30.0)  # Continuous Assessment
    exam_weight = models.FloatField(default=70.0)
    
    # Staff
    lecturer = models.ForeignKey('students.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='courses_taught')
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'courses'
        unique_together = ['university', 'code', 'level']
    
    def __str__(self):
        return f"{self.code} - {self.title}"


class CourseMaterial(models.Model):
    """Course materials and resources"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # File
    file = models.FileField(upload_to='course_materials/')
    file_type = models.CharField(max_length=50)  # PDF, Video, etc.
    
    # For video streaming
    video_url = models.URLField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    # Accessibility
    is_offline_available = models.BooleanField(default=False)
    
    uploaded_by = models.ForeignKey('students.User', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'course_materials'
        ordering = ['-uploaded_at']


class Enrollment(models.Model):
    """Student course enrollment"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        DROPPED = 'dropped', 'Dropped'
        FAILED = 'failed', 'Failed'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='enrollments')
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # For American system
    grade = models.CharField(max_length=5, blank=True)
    grade_points = models.FloatField(null=True, blank=True)
    
    # For American: letter grade, pass/fail, etc.
    grading_option = models.CharField(max_length=20, blank=True)  # Letter, Pass/Fail
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    dropped_at = models.DateTimeField(null=True, blank=True)
    
    # For dropped courses
    drop_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'course', 'semester']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"


class Grade(models.Model):
    """Student grades with system-aware grading"""
    
    class GradeStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUBMITTED = 'submitted', 'Submitted'
        APPROVED = 'approved', 'Approved'
        APPEALED = 'appealed', 'Appealed'
        MODIFIED = 'modified', 'Modified'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='grade_record')
    
    # Scores
    ca_score = models.FloatField(null=True, blank=True, help_text="Continuous Assessment")
    midterm_score = models.FloatField(null=True, blank=True)
    exam_score = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    
    # Grade
    grade = models.CharField(max_length=5, blank=True)
    grade_points = models.FloatField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=GradeStatus.choices, default=GradeStatus.PENDING)
    
    # Staff
    entered_by = models.ForeignKey('students.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='grades_entered')
    approved_by = models.ForeignKey('students.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='grades_approved')
    
    entered_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Comments
    comments = models.TextField(blank=True)
    
    class Meta:
        db_table = 'grades'
    
    def save(self, *args, **kwargs):
        if self.ca_score is not None and self.exam_score is not None:
            enrollment = self.enrollment
            ca_weight = enrollment.course.ca_weight / 100
            exam_weight = enrollment.course.exam_weight / 100
            
            self.total_score = (self.ca_score * ca_weight) + (self.exam_weight * exam_weight)
            self.grade = self.calculate_grade(self.total_score, enrollment.student.university)
        
        super().save(*args, **kwargs)
    
    def calculate_grade(self, score, university):
        """Calculate letter grade based on university system"""
        grading = university.get_grading_config()
        
        for grade, config in grading.items():
            if config['min'] <= score <= config['max']:
                return grade
        
        return 'F'


class GradeAppeal(models.Model):
    """Student grade appeal"""
    
    class AppealStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        UNDER_REVIEW = 'under_review', 'Under Review'
        RESOLVED = 'resolved', 'Resolved'
        REJECTED = 'rejected', 'Rejected'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='appeals')
    
    reason = models.TextField()
    supporting_documents = models.FileField(upload_to='appeals/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=AppealStatus.choices, default=AppealStatus.PENDING)
    
    resolution = models.TextField(blank=True)
    resolved_by = models.ForeignKey('students.User', null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    appealed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'grade_appeals'


class Timetable(models.Model):
    """Course timetable"""
    
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='timetables')
    
    # Venue
    venue = models.ForeignKey('academic.Venue', on_delete=models.CASCADE, related_name='timetables')
    
    # Time
    day = models.CharField(max_length=20, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # For American: section
    section = models.CharField(max_length=10, blank=True)
    
    # Lecturer
    lecturer = models.ForeignKey('students.User', null=True, blank=True, on_delete=models.SET_NULL)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'timetables'
        unique_together = ['course', 'semester', 'day', 'start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.day} {self.start_time}-{self.end_time}"


class Venue(models.Model):
    """Exam/Lecture venue"""
    
    class VenueType(models.TextChoices):
        LECTURE_HALL = 'lecture_hall', 'Lecture Hall'
        LABORATORY = 'laboratory', 'Laboratory'
        EXAM_HALL = 'exam_hall', 'Exam Hall'
        AUDITORIUM = 'auditorium', 'Auditorium'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='venues')
    
    name = models.CharField(max_length=100)  # e.g., LT1, LAB 1
    building = models.CharField(max_length=100)
    venue_type = models.CharField(max_length=20, choices=VenueType.choices)
    
    capacity = models.IntegerField()
    exam_capacity = models.IntegerField(default=0)  # Reduced for exams
    
    # For exams
    can_host_exams = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'venues'
    
    def __str__(self):
        return f"{self.name} ({self.building})"


class Hostel(models.Model):
    """Hostel/Accommodation"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='hostels')
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    gender = models.CharField(max_length=10)  # Male, Female, Mixed
    
    # Capacity
    total_beds = models.IntegerField()
    occupied_beds = models.IntegerField(default=0)
    
    # For Nigerian: male/female wings
    wing = models.CharField(max_length=20, blank=True)
    
    warden = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hostels'
    
    def __str__(self):
        return f"{self.name} ({self.gender})"
    
    @property
    def available_beds(self):
        return self.total_beds - self.occupied_beds


class HostelApplication(models.Model):
    """Student hostel application"""
    
    class ApplicationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        ALLOCATED = 'allocated', 'Allocated'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_applications')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='hostel_applications')
    
    # Preferences
    first_choice = models.ForeignKey(Hostel, null=True, blank=True, on_delete=models.SET_NULL, related_name='first_choice_apps')
    second_choice = models.ForeignKey(Hostel, null=True, blank=True, on_delete=models.SET_NULL, related_name='second_choice_apps')
    
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    
    # Allocation
    allocated_hostel = models.ForeignKey(Hostel, null=True, blank=True, on_delete=models.SET_NULL, related_name='allocated_students')
    room_number = models.CharField(max_length=20, blank=True)
    bed_number = models.CharField(max_length=10, blank=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'hostel_applications'
        unique_together = ['student', 'semester']


class ExamSitting(models.Model):
    """Exam timetable and seating"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_sittings')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='exam_sittings')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='exam_sittings')
    
    # Seating
    invigilator = models.ForeignKey('students.User', null=True, blank=True, on_delete=models.SET_NULL)
    
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'exam_sittings'
        unique_together = ['course', 'semester', 'date']


class ExamResult(models.Model):
    """Student exam seating"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    exam_sitting = models.ForeignKey(ExamSitting, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_sittings')
    
    seat_number = models.CharField(max_length=10)
    
    # For misconduct
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'exam_results'
        unique_together = ['exam_sitting', 'student']