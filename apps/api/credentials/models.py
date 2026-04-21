"""
Digital Credentials Models
Blockchain-based credentials verification
"""
import hashlib
import uuid
from django.db import models
from django.conf import settings


class CredentialType(models.TextChoices):
    CERTIFICATE = 'certificate', 'Certificate'
    TRANSCRIPT = 'transcript', 'Transcript'
    DEGREE = 'degree', 'Degree'
    DIPLOMA = 'diploma', 'Diploma'
    BADGE = 'badge', 'Digital Badge'
    CERTIFICATION = 'certification', 'Professional Certification'


class CredentialStatus(models.TextChoices):
    ISSUED = 'issued', 'Issued'
    REVOKED = 'revoked', 'Revoked'
    EXPIRED = 'expired', 'Expired'
    PENDING = 'pending', 'Pending Verification'


class Credential(models.Model):
    """Digital credential"""
    credential_id = models.UUIDField(default=uuid.uuid4, unique=True)
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='credentials'
    )
    credential_type = models.CharField(max_length=20, choices=CredentialType.choices)
    
    # Credential details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    issued_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # Programme/Course info
    programme = models.ForeignKey(
        'university.Programme',
        on_delete=models.SET_NULL,
        null=True,
        related_name='credentials'
    )
    level = models.CharField(max_length=20, blank=True)
    grade_classification = models.CharField(max_length=50, blank=True)
    
    # Verification
    status = models.CharField(
        max_length=20,
        choices=CredentialStatus.choices,
        default=CredentialStatus.ISSUED
    )
    verification_hash = models.CharField(max_length=255, unique=True)
    blockchain_txid = models.CharField(max_length=255, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict)
    issuing_authority = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_credentials'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'digital_credentials'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.credential_id} - {self.title}"
    
    def generate_hash(self):
        """Generate verification hash"""
        data = f"{self.credential_id}{self.student.matric_number}{self.title}{self.issued_date}"
        return hashlib.sha256(data.encode()).hexdigest()


class CredentialVerification(models.Model):
    """Track credential verifications"""
    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name='verifications'
    )
    verifier_name = models.CharField(max_length=255)
    verifier_email = models.EmailField(blank=True)
    verifier_organization = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField()

    class Meta:
        db_table = 'credential_verifications'
        ordering = ['-verified_at']

    def __str__(self):
        return f"{self.credential.credential_id} - {self.verifier_name}"


class BlockchainRecord(models.Model):
    """Blockchain transaction records"""
    credential = models.OneToOneField(
        Credential,
        on_delete=models.CASCADE,
        related_name='blockchain_record'
    )
    network = models.CharField(max_length=50)  # ethereum, polygon, etc.
    transaction_hash = models.CharField(max_length=255, unique=True)
    block_number = models.BigIntegerField()
    block_timestamp = models.DateTimeField()
    contract_address = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255, blank=True)
    metadata_uri = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = 'blockchain_records'

    def __str__(self):
        return f"{self.network} - {self.transaction_hash[:10]}..."