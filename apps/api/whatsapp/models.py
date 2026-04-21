"""
WhatsApp Integration Models
WhatsApp Business API integration
"""
import uuid
from django.db import models
from django.conf import settings


class MessageType(models.TextChoices):
    TEXT = 'text', 'Text'
    IMAGE = 'image', 'Image'
    DOCUMENT = 'document', 'Document'
    VIDEO = 'video', 'Video'
    AUDIO = 'audio', 'Audio'
    Sticker = 'sticker', 'Sticker'
    INTERACTIVE = 'interactive', 'Interactive'
    TEMPLATE = 'template', 'Template'


class MessageStatus(models.TextChoices):
    QUEUED = 'queued', 'Queued'
    SENT = 'sent', 'Sent'
    DELIVERED = 'delivered', 'Delivered'
    READ = 'read', 'Read'
    FAILED = 'failed', 'Failed'


class TemplateCategory(models.TextChoices):
    ADMISSION = 'admission', 'Admission'
    PAYMENT = 'payment', 'Payment'
    ACADEMIC = 'academic', 'Academic'
    RESULT = 'result', 'Result'
    ANNOUNCEMENT = 'announcement', 'Announcement'
    REMINDER = 'reminder', 'Reminder'
    ALERT = 'alert', 'Alert'


class WhatsAppTemplate(models.Model):
    """WhatsApp message templates"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='whatsapp_templates'
    )
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=TemplateCategory.choices)
    language = models.CharField(max_length=10, default='en')
    
    # Template content
    header = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    footer = models.CharField(max_length=255, blank=True)
    buttons = models.JSONField(default=list)
    
    # Variables
    variables = models.JSONField(default=list)  # List of variable names
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'whatsapp_templates'
        ordering = ['name']

    def __str__(self):
        return self.name


class WhatsAppContact(models.Model):
    """WhatsApp contacts"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='whatsapp_contacts'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='whatsapp_contacts',
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    is_opted_in = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'whatsapp_contacts'
        unique_together = ['university', 'phone']

    def __str__(self):
        return f"{self.phone} - {self.name}"


class WhatsAppMessage(models.Model):
    """WhatsApp messages"""
    message_id = models.UUIDField(default=uuid.uuid4, unique=True)
    contact = models.ForeignKey(
        WhatsAppContact,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # Message details
    message_type = models.CharField(max_length=20, choices=MessageType.choices)
    content = models.TextField()
    media_url = models.URLField(max_length=500, blank=True)
    media_id = models.CharField(max_length=255, blank=True)
    
    # Template info
    template = models.ForeignKey(
        WhatsAppTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )
    template_vars = models.JSONField(default=dict)
    
    # Direction
    direction = models.CharField(
        max_length=10,
        choices=[
            ('inbound', 'Inbound'),
            ('outbound', 'Outbound')
        ]
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=MessageStatus.choices,
        default=MessageStatus.QUEUED
    )
    wamid = models.CharField(max_length=255, blank=True)  # WhatsApp message ID
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'whatsapp_messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.message_id} - {self.direction}"


class WhatsAppCampaign(models.Model):
    """WhatsApp broadcast campaigns"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='whatsapp_campaigns'
    )
    name = models.CharField(max_length=255)
    template = models.ForeignKey(
        WhatsAppTemplate,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    
    # Target
    target_filter = models.JSONField(default=dict)  # Filter criteria
    
    # Campaign details
    message = models.TextField(blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    
    # Stats
    total_recipients = models.IntegerField(default=0)
    delivered = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('sending', 'Sending'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='draft'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'whatsapp_campaigns'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ChatbotSession(models.Model):
    """AI Chatbot sessions"""
    contact = models.ForeignKey(
        WhatsAppContact,
        on_delete=models.CASCADE,
        related_name='chatbot_sessions'
    )
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    
    # State
    state = models.CharField(
        max_length=50,
        default='greeting'
    )
    context = models.JSONField(default=dict)
    
    # Messages
    message_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'chatbot_sessions'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.session_id} - {self.contact.phone}"