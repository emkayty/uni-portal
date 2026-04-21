"""
LMS Integration Models
Supports Blackboard, Canvas, Moodle integration
"""
from django.db import models
from django.conf import settings


class LMSProvider(models.TextChoices):
    BLACKBOARD = 'blackboard', 'Blackboard Learn'
    CANVAS = 'canvas', 'Canvas LMS'
    MOODLE = 'moodle', 'Moodle'


class LMSInstance(models.Model):
    """LMS Instance for a university"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='lms_instances'
    )
    provider = models.CharField(
        max_length=20,
        choices=LMSProvider.choices,
        default=LMSProvider.BLACKBOARD
    )
    base_url = models.URLField(max_length=500)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    client_id = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lms_instances'

    def __str__(self):
        return f"{self.university.name} - {self.get_provider_display()}"


class CourseMapping(models.Model):
    """Mapping between local courses and LMS courses"""
    local_course = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        related_name='lms_mappings'
    )
    lms_instance = models.ForeignKey(
        LMSInstance,
        on_delete=models.CASCADE,
        related_name='course_mappings'
    )
    lms_course_id = models.CharField(max_length=200)
    lms_course_url = models.URLField(max_length=500, blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('synced', 'Synced'),
            ('failed', 'Failed')
        ],
        default='pending'
    )

    class Meta:
        db_table = 'lms_course_mappings'
        unique_together = ['local_course', 'lms_instance']

    def __str__(self):
        return f"{self.local_course.code} -> {self.lms_course_id}"


class ContentItem(models.Model):
    """Lecture content from LMS"""
    course_mapping = models.ForeignKey(
        CourseMapping,
        on_delete=models.CASCADE,
        related_name='content_items'
    )
    lms_content_id = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('file', 'File'),
            ('video', 'Video'),
            ('link', 'External Link'),
            ('page', 'Page'),
            ('assignment', 'Assignment'),
            ('quiz', 'Quiz')
        ]
    )
    url = models.URLField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # seconds for video
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lms_content_items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.content_type})"


class VideoRecording(models.Model):
    """Video lecture recordings"""
    content_item = models.OneToOneField(
        ContentItem,
        on_delete=models.CASCADE,
        related_name='video_recording'
    )
    video_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    duration_seconds = models.IntegerField()
    resolutions = models.JSONField(default=list)  # ['240p', '360p', '720p', '1080p']
    transcript = models.TextField(blank=True)
    subtitles = models.JSONField(default=dict)  # {'en': url, 'ha': url}

    class Meta:
        db_table = 'lms_video_recordings'

    def __str__(self):
        return f"Video: {self.content_item.title}"


class EnrollmentSync(models.Model):
    """Track LMS enrollment sync status"""
    enrollment = models.ForeignKey(
        'academic.Enrollment',
        on_delete=models.CASCADE,
        related_name='lms_sync'
    )
    lms_instance = models.ForeignKey(
        LMSInstance,
        on_delete=models.CASCADE,
        related_name='enrollment_syncs'
    )
    lms_user_id = models.CharField(max_length=200)
    lms_enrollment_id = models.CharField(max_length=200)
    synced_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('enrolled', 'Enrolled'),
            ('dropped', 'Dropped'),
            ('failed', 'Failed')
        ],
        default='pending'
    )

    class Meta:
        db_table = 'lms_enrollment_sync'
        unique_together = ['enrollment', 'lms_instance']

    def __str__(self):
        return f"{self.enrollment.student.matric_number} - {self.status}"


class GradeSync(models.Model):
    """Sync grades between local system and LMS"""
    enrollment = models.ForeignKey(
        'academic.Enrollment',
        on_delete=models.CASCADE,
        related_name='grade_syncs'
    )
    lms_instance = models.ForeignKey(
        LMSInstance,
        on_delete=models.CASCADE,
        related_name='grade_syncs'
    )
    lms_grade_id = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    synced_at = models.DateTimeField(auto_now=True)
    direction = models.CharField(
        max_length=10,
        choices=[
            ('to_lms', 'To LMS'),
            ('from_lms', 'From LMS')
        ],
        default='to_lms'
    )

    class Meta:
        db_table = 'lms_grade_sync'

    def __str__(self):
        return f"{self.enrollment.course.code} - {self.score}"


class Announcement(models.Model):
    """LMS Announcements"""
    course_mapping = models.ForeignKey(
        CourseMapping,
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    title = models.CharField(max_length=500)
    message = models.TextField()
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lms_announcements'
        ordering = ['-created_at']

    def __str__(self):
        return self.title