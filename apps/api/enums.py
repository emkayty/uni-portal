"""
STANDARD ENUMERATIONS - UNIVERSITY PORTAL
=====================================
All standardized enums aligned with Nigerian & global standards

Version: 2.0.0
"""

from enum import Enum


# =============================================================================
# ACADEMIC ENUMS
# =============================================================================
class AcademicStatus(str, Enum):
    """Student academic status"""
    ACTIVE = "Active"
    GRADUATED = "Graduated"
    SUSPENDED = "Suspended"
    WITHDRAWN = "Withdrawn"
    PROBATION = "Probation"
    DEFERRD = "Deferred"


class SemesterType(str, Enum):
    """Academic semester"""
    FIRST = "First"
    SECOND = "Second"
    RAIN = "Rain"


class CourseType(str, Enum):
    """Course classification"""
    CORE = "core"
    ELECTIVE = "elective"
    GENERAL = "general"
    FOUNDATION = "foundation"


class CourseStatus(str, Enum):
    """Enrollment status"""
    REGISTERED = "Registered"
    DROPPED = "Dropped"
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"


class GradeStatus(str, Enum):
    """Grade submission status"""
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    PUBLISHED = "Published"
    APPEALED = "Appealed"


# =============================================================================
# ADMISSION ENUMS
# =============================================================================
class AdmissionStatus(str, Enum):
    """Admission application status"""
    PENDING = "Pending"
    SCREENING = "Screening"
    OFFERED = "Offered"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    DEFERRED = "Deferred"


class ApplicationMode(str, Enum):
    """Application mode"""
    UTME = "UTME"
    DIRECT = "Direct Entry"
    TRANSFER = "Transfer"
    POST_UTME = "Post-UTME"


# =============================================================================
# FINANCIAL ENUMS
# =============================================================================
class PaymentStatus(str, Enum):
    """Payment status"""
    PENDING = "Pending"
    INITIATED = "Initiated"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class InvoiceStatus(str, Enum):
    """Invoice status"""
    DRAFT = "Draft"
    GENERATED = "Generated"
    PARTIAL = "Partial"
    PAID = "Paid"
    OVERDUE = "Overdue"
    CANCELLED = "Cancelled"


class TransactionType(str, Enum):
    """Financial transaction type"""
    FEE = "Fee"
    FINE = "Fine"
    SCHOLARSHIP = "Scholarship"
    REFUND = "Refund"
    OTHER = "Other"


# =============================================================================
# EXAM ENUMS
# =============================================================================
class ExamStatus(str, Enum):
    """Exam session status"""
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    POSTPONED = "Postponed"


class VenueStatus(str, Enum):
    """Venue booking status"""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"


# =============================================================================
# ATTENDANCE ENUMS
# =============================================================================
class AttendanceStatus(str, Enum):
    """Attendance status"""
    PRESENT = "Present"
    ABSENT = "Absent"
    EXCUSED = "Excused"
    LATE = "Late"
    ABSENT_WITH_LEAVE = "Absent with Leave"


# =============================================================================
# LIBRARY ENUMS
# =============================================================================
class LoanStatus(str, Enum):
    """Library loan status"""
    AVAILABLE = "Available"
    ON_LOAN = "On Loan"
    RESERVED = "Reserved"
    OVERDUE = "Overdue"
    LOST = "Lost"


class ReservationStatus(str, Enum):
    """Book reservation status"""
    PENDING = "Pending"
    READY = "Ready"
    COLLECTED = "Collected"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"


# =============================================================================
# CLEARANCE ENUMS
# =============================================================================
class ClearanceStatus(str, Enum):
    """Clearance status"""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COMPLETED = "Completed"


class ClearanceType(str, Enum):
    """Clearance type"""
    DEPARTMENT = "Department"
    LIBRARY = "Library"
    FINANCE = "Finance"
    HOSTEL = "Hostel"
    SIWES = "SIWES"
    FINAL = "Final"


# =============================================================================
# SIWES ENUMS
# =============================================================================
class SIWESStatus(str, Enum):
    """SIWES status"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    EXTENDED = "Extended"
    TERMINATED = "Terminated"


# =============================================================================
# USER ENUMS (NIGERIAN CONTEXT)
# =============================================================================
class Gender(str, Enum):
    """Gender"""
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class Nationality(str, Enum):
    """Nationality type"""
    NIGERIAN = "Nigerian"
    FOREIGNER = "Foreigner"


class MaritalStatus(str, Enum):
    """Marital status"""
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    PENDING = "Pending"
    ARCHIVED = "Archived"


# =============================================================================
# NOTIFICATION ENUMS
# =============================================================================
class NotificationChannel(str, Enum):
    """Notification channel"""
    EMAIL = "Email"
    SMS = "SMS"
    WHATSAPP = "WhatsApp"
    PUSH = "Push"
    IN_APP = "In-App"


class NotificationPriority(str, Enum):
    """Notification priority"""
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    URGENT = "Urgent"


# =============================================================================
# DOCUMENT ENUMS
# =============================================================================
class DocumentType(str, Enum):
    """Document types"""
    CERTIFICATE = "Certificate"
    TRANSCRIPT = "Transcript"
    ID_CARD = "ID Card"
    ADMISSION_LETTER = "Admission Letter"
    ACCEPTANCE = "Acceptance"
    RESULT = "Result"
    OTHER = "Other"


class DocumentStatus(str, Enum):
    """Document status"""
    UPLOADED = "Uploaded"
    PENDING = "Pending"
    VERIFIED = "Verified"
    REJECTED = "Rejected"


# =============================================================================
# CREDENTIAL ENUMS
# =============================================================================
class CredentialType(str, Enum):
    """Digital credential type"""
    CERTIFICATE = "Certificate"
    DIPLOMA = "Diploma"
    DEGREE = "Degree"
    TRANSCRIPT = "Transcript"
    VERIFICATION = "Verification"


class VerificationStatus(str, Enum):
    """Verification status"""
    VERIFIED = "Verified"
    UNVERIFIED = "Unverified"
    EXPIRED = "Expired"
    REVOKED = "Revoked"


# =============================================================================
# JOB APPLICATION ENUMS
# =============================================================================
class JobStatus(str, Enum):
    """Job posting status"""
    DRAFT = "Draft"
    ACTIVE = "Active"
    CLOSED = "Closed"
    EXPIRED = "Expired"


class ApplicationStatus(str, Enum):
    """Application status"""
    APPLIED = "Applied"
    SCREENING = "Screening"
    SHORTLISTED = "Shortlisted"
    INTERVIEW = "Interview"
    OFFERED = "Offered"
    REJECTED = "Rejected"


# =============================================================================
# ALUMNI ENUMS
# =============================================================================
class AlumniCategory(str, Enum):
    """Alumni category"""
    GRADUATE = "Graduate"
    DROPOUT = "Drop-out"
    TRANSFERRED = "Transferred"


# =============================================================================
# EXPORT ALL
# =============================================================================
__all__ = [
    # Academic
    "AcademicStatus", "SemesterType", "CourseType", "CourseStatus", "GradeStatus",
    # Admission
    "AdmissionStatus", "ApplicationMode",
    # Finance
    "PaymentStatus", "InvoiceStatus", "TransactionType",
    # Exam
    "ExamStatus", "VenueStatus",
    # Attendance
    "AttendanceStatus",
    # Library
    "LoanStatus", "ReservationStatus",
    # Clearance
    "ClearanceStatus", "ClearanceType",
    # SIWES
    "SIWESStatus",
    # User
    "Gender", "Nationality", "MaritalStatus", "UserStatus",
    # Notification
    "NotificationChannel", "NotificationPriority",
    # Document
    "DocumentType", "DocumentStatus",
    # Credential
    "CredentialType", "VerificationStatus",
    # Job
    "JobStatus", "ApplicationStatus",
    # Alumni
    "AlumniCategory",
    # Helper function
    "get_status_choices", "get_enum_choices"
]


def get_status_choices(enum_class) -> list[dict]:
    """Get choices from enum"""
    return [{"value": e.value, "label": e.value} for e in enum_class]


def get_enum_choices(enum_class) -> list[tuple]:
    """Get Django choices format"""
    return [(e.value, e.value) for e in enum_class]