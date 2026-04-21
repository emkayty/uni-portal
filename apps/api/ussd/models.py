"""
USSD Models
Unstructured Supplementary Service Data
"""
from django.db import models
from django.conf import settings


class UssdMenu(models.Model):
    """USSD menu structure"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='ussd_menus'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)  # e.g., *394#
    
    # Menu structure
    entry_point = models.CharField(max_length=50, default='main')
    menu_tree = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ussd_menus'
        unique_together = ['university', 'code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class UssdSession(models.Model):
    """USSD session tracking"""
    session_id = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='ussd_sessions'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ussd_sessions'
    )
    
    # Session state
    current_menu = models.CharField(max_length=50)
    previous_menu = models.CharField(max_length=50, blank=True)
    input_data = models.JSONField(default=dict)
    
    # Status
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ussd_sessions'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.phone} - {self.current_menu}"


class UssdLog(models.Model):
    """USSD request/response logs"""
    session = models.ForeignKey(
        UssdSession,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    menu = models.CharField(max_length=50)
    user_input = models.TextField(blank=True)
    response = models.TextField()
    duration_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ussd_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.session.phone} - {self.menu}"