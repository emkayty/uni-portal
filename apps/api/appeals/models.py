"""
Grade Appeal Models
Student grade appeal workflow system
"""
from django.db import models
from django.conf import settings


class AppealReason(models.TextChoices):
    MARKING_ERROR = 'marking_error', 'Marking Error'
    GRADING_GUIDELINES = 'grading_guidelines', 'Grading Guidelines Not Followed'
    CALCULATION_ERROR = 'calculation_error', 'Calculation Error'
    MISSING_WORK = 'missing_work', 'Missing Work Not Considered'
    EXAMINATION_CONDITIONS = 'examination_conditions', 'Examination Conditions'
    MEDICAL_GROUND = 'medical_ground', 'Medical Grounds'
    OTHER = 'other', 'Other'


class AppealStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Review'
    UNDER_REVIEW = 'under_review', 'Under Review'
    ADDITIONAL_INFO = 'additional_info', 'Additional Information Required'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    ESCALATED = 'escalated', 'Escalated to Senate'


class GradeAppeal(models.Model):
    """Student grade appeal"""
    enrollment = models.ForeignKey(
        'academic.Enrollment',
        on_delete=models.CASCADE,
        related_name='grade_appeals'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='grade_appeals'
    )
    course = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        related_name='grade_appeals'
    )
    
    # Appeal details
    reason = models.CharField(max_length=50, choices=AppealReason.choices)
    description = models.TextField()
    expected_grade = models.CharField(max_length=5)
    actual_grade = models.CharField(max_length=5)
    
    # Evidence
    evidence_files = models.JSONField(default=list)  # List of file URLs
    supporting_documents = models.JSONField(default=list)
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=AppealStatus.choices,
        default=AppealStatus.PENDING
    )
    
    # Review information
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_appeals'
    )
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolved_grade = models.CharField(max_length=5, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'grade_appeals_new'
        ordering = ['-created_at']
        unique_together = ['enrollment', 'course']

    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code} appeal"


class AppealEvidence(models.Model):
    """Evidence documents for appeals"""
    appeal = models.ForeignKey(
        GradeAppeal,
        on_delete=models.CASCADE,
        related_name='evidence'
    )
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=500)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appeal_evidence'

    def __str__(self):
        return f"{self.file_name} - {self.appeal.id}"


class AppealComment(models.Model):
    """Comments on appeals"""
    appeal = models.ForeignKey(
        GradeAppeal,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appeal_comments'
    )
    content = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appeal_comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.appeal.id}"


class AppealTimeline(models.Model):
    """Timeline of appeal status changes"""
    appeal = models.ForeignKey(
        GradeAppeal,
        on_delete=models.CASCADE,
        related_name='timeline'
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    notes = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appeal_timeline'
        ordering = ['changed_at']

    def __str__(self):
        return f"{self.appeal.id}: {self.from_status} -> {self.to_status}"


class GradeReviewCommittee(models.Model):
    """Grade review committee members"""
    university = models.ForeignKey(
        'university.University',
        on_delete=models.CASCADE,
        related_name='grade_committees'
    )
    members = models.JSONField(default=list)  # List of user IDs
    chair = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='chaired_committees'
    )
    academic_session = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'grade_review_committees'
        unique_together = ['university', 'academic_session']

    def __str__(self):
        return f"Committee {self.university.name} - {self.academic_session}"