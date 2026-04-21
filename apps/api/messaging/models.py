"""
Messaging Models
Announcements, notifications, messages
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Announcement(models.Model):
    """System-wide announcements"""
    
    class Category(models.TextChoices):
        GENERAL = 'general', 'General'
        ACADEMIC = 'academic', 'Academic'
        ADMINISTRATIVE = 'administrative', 'Administrative'
        FINANCIAL = 'financial', 'Financial'
        EVENT = 'event', 'Event'
        EMERGENCY = 'emergency', 'Emergency'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        NORMAL = 'normal', 'Normal'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    class TargetAudience(models.TextChoices):
        ALL = 'all', 'All'
        STUDENTS = 'students', 'Students'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Admin'
        DEPARTMENT = 'department', 'Department'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    target_audience = models.CharField(max_length=20, choices=TargetAudience.choices, default=TargetAudience.ALL)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Notification(models.Model):
    """User-specific notifications"""
    
    class NotificationType(models.TextChoices):
        INFO = 'info', 'Information'
        SUCCESS = 'success', 'Success'
        WARNING = 'warning', 'Warning'
        ERROR = 'error', 'Error'
        SYSTEM = 'system', 'System'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()  # Link to User or Student
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user_id}"


class Message(models.Model):
    """Internal messaging between users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.UUIDField()
    recipient_id = models.UUIDField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} -> {self.recipient_id}"