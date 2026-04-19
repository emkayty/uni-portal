"""
User/Staff Models
Staff, roles, permissions for university staff
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Staff(AbstractUser):
    """Staff model extending User"""
    
    class StaffType(models.TextChoices):
        ACADEMIC = 'academic', 'Academic'
        ADMINISTRATIVE = 'administrative', 'Administrative'
        TECHNICAL = 'technical', 'Technical'
        SUPPORT = 'support', 'Support'
    
    class Designation(models.TextChoices):
        PROFESSOR = 'professor', 'Professor'
        ASSOCIATE_PROFESSOR = 'associate_professor', 'Associate Professor'
        SENIOR_LECTURER = 'senior_lecturer', 'Senior Lecturer'
        LECTURER = 'lecturer', 'Lecturer'
        ASSISTANT_LECTURER = 'assistant_lecturer', 'Assistant Lecturer'
        TUTOR = 'tutor', 'Tutor'
        LAB_TECHNICIAN = 'lab_technician', 'Lab Technician'
        REGISTRAR = 'registrar', 'Registrar'
        DEPUTY_REGISTRAR = 'deputy_registrar', 'Deputy Registrar'
        DIRECTOR = 'director', 'Director'
        ADMIN_OFFICER = 'admin_officer', 'Admin Officer'
    
    # Link to User
    user = models.OneToOneField(AbstractUser, on_delete=models.CASCADE, parent_link=True)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='staff')
    
    staff_type = models.CharField(max_length=20, choices=StaffType.choices)
    designation = models.CharField(max_length=30, choices=Designation.choices)
    
    # Department
    department = models.ForeignKey('university.Department', null=True, blank=True, on_delete=models.SET_NULL, related_name='staff')
    
    # Staff ID
    staff_id = models.CharField(max_length=20, unique=True)
    
    # Academic info (for lecturers)
    highest_qualification = models.CharField(max_length=50, blank=True)
    area_of_specialization = models.CharField(max_length=200, blank=True)
    
    # Employment
    employment_date = models.DateField(null=True, blank=True)
    confirmation_date = models.DateField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    # For Nigerian: CONMESS (academic)
    conmess_level = models.CharField(max_length=20, blank=True)  # CONMESS 1-15
    
    # Access levels
    can_enter_grades = models.BooleanField(default=False)
    can_approve_grades = models.BooleanField(default=False)
    can_register_students = models.BooleanField(default=False)
    can_view_financials = models.BooleanField(default=False)
    can_issue_clearance = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'staff'
    
    def __str__(self):
        return f"{self.staff_id} - {self.get_full_name()}"


class Role(models.Model):
    """Roles for access control"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    university = models.ForeignKey('university.University', on_delete=models.CASCADE, related_name='roles')
    
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    
    # Permissions
    can_manage_students = models.BooleanField(default=False)
    can_manage_courses = models.BooleanField(default=False)
    can_manage_grades = models.BooleanField(default=False)
    can_manage_finance = models.BooleanField(default=False)
    can_manage_admission = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_manage_settings = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'roles'
        unique_together = ['university', 'code']


class UserRole(models.Model):
    """User role assignments"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    
    assigned_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='role_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_roles'
        unique_together = ['user', 'role']


class Permission(models.Model):
    """Granular permissions"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='permissions')
    
    # Resource
    resource = models.CharField(max_length=50)  # students, courses, grades, etc.
    resource_id = models.UUIDField(null=True, blank=True)
    
    # Action
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    
    granted_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='permission_grants')
    granted_at = models.DateTimeField(auto_now_add=True)
    
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_permissions'


class AuditLog(models.Model):
    """Audit trail for all user actions"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=50)
    resource_id = models.UUIDField(null=True, blank=True)
    
    details = models.JSONField(default=dict)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['resource', 'resource_id']),
        ]