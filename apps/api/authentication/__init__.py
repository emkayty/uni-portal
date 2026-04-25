"""
Authentication Module for University Portal
Provides JWT-based authentication with role-based access control
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum

# Fix JWT import for different versions
try:
    import jwt
except ImportError:
    import PyJWT as jwt

from pydantic import BaseModel, Field, field_validator


# ============= CONSTANTS =============
JWT_SECRET = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


# ============= NIGERIAN STATES =============
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", 
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", 
    "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", 
    "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", 
    "Osun", "Oyo", "Plateau", "Sokoto", "Taraba", "Yobe", "Zamfara",
    "Federal Capital Territory"
]

NIGERIAN_LOCAL_GOVERNMENTS = {
    "Lagos": ["Agege", "Alimosho", "Amuwo-Odofin", "Apapa", "Badagry", "Epe", "Eti-Osa", "Ibeju-Lekki", "Ifako-Ijaye", "Ikeja", "Ikorodu", "Kosofe", "Lagos Island", "Lagos Mainland", "Mushin", "Ojo", "Shomolu", "Surulere"],
    "Kano": ["Ajingi", "Albasu", "Bagwai", "Bebi", "Bunkure", "Dala", "Dambatta", "Dan Musa", "Darako", "Dawakin Kudu", "Dawakin Tofa", "Doguwa", "Fab-com", "Gaya", "Gezawa", "Gwarzo", "Kabo", "K市长", "Kura", "Madobi", "Makoda", "Minjibir", "Nasarawa", "Rano", "Rimin Gata", "Rogo", "Sumaila", "Takai", "Tofa", "Tsanyawa", "Tudun Wada", "Ungogo", "Warawa", "Wudil"],
    # Add more as needed
}

NIGERIAN_COUNTRIES = [
    "Nigeria", "Ghana", "Togo", "Benin", "Cote d'Ivoire", "Senegal", "Mali", "Niger", "Cameroon", 
    "Chad", "Sudan", "Egypt", "Morocco", "South Africa", "Kenya", "Uganda", "Tanzania",
    "United Kingdom", "United States", "Canada", "Germany", "France", "Italy", "Spain",
    "China", "India", "Japan", "South Korea", "Saudi Arabia", "UAE", "USA"
]


# ============= ENUMS =============
class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    LECTURER = "lecturer"
    FINANCE_OFFICER = "finance_officer"
    DEAN = "dean"
    HOD = "hod"
    REGISTRAR = "registrar"


class Nationality(str, Enum):
    NIGERIAN = "Nigerian"
    FOREIGNER = "Foreigner"


class MaritalStatus(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


# ============= NIGERIAN-SPECIFIC MODELS =============
class Address(BaseModel):
    """Nigerian address model"""
    street_address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    local_government: Optional[str] = Field(None, description="Local Government Area")
    state: str = Field(..., description="State of Nigeria")
    postal_code: Optional[str] = Field(None, description="Postal code")
    country: str = Field(default="Nigeria", description="Country")


class GuardianInfo(BaseModel):
    """Guardian/Parent information for Nigerian students"""
    full_name: str = Field(..., description="Guardian full name")
    relationship: str = Field(..., description="Relationship to student (Father, Mother, Guardian, etc.)")
    phone_number: str = Field(..., description="Guardian phone number (11 digits)")
    alternate_phone: Optional[str] = Field(None, description="Alternate phone number")
    email: Optional[str] = Field(None, description="Guardian email address")
    occupation: Optional[str] = Field(None, description="Occupation")
    address: Optional[Address] = None
    is_emergency_contact: bool = Field(default=True, description="Can be contacted in emergencies")


class StudentProfile(BaseModel):
    """Comprehensive Nigerian student profile"""
    # Personal Information
    gender: Gender
    date_of_birth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    place_of_birth: Optional[str] = Field(None, description="Place of birth")
    
    # Nationality & Identity
    nationality: Nationality = Field(default=Nationality.NIGERIAN)
    state_of_origin: Optional[str] = Field(None, description="State of Origin", examples=NIGERIAN_STATES)
    local_government: Optional[str] = Field(None, description="Local Government Area")
    nin: Optional[str] = Field(None, description="National Identification Number (11 digits)", examples=["12345678901"])
    bvn: Optional[str] = Field(None, description="Bank Verification Number (11 digits)")
    
    # Contact Information
    phone_number: str = Field(..., description="Personal phone number")
    alternate_phone: Optional[str] = Field(None, description="Alternate phone")
    email: str = Field(..., description="Email address")
    home_address: Optional[Address] = None
    mailing_address: Optional[Address] = None
    
    # Guardian Information
    guardian: Optional[GuardianInfo] = None
    
    # Additional Information
    marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    religion: Optional[str] = Field(None, description=" Religion (Christian, Muslim, Others)")
    blood_group: Optional[str] = Field(None, description="Blood group (A+, A-, B+, B-, O+, O-, AB+, AB-)")
    genotype: Optional[str] = Field(None, description="Genotype (AA, AS, SS, AC)")
    disability: Optional[str] = Field(None, description="Any disability or special needs")
    
    # Foreigner-specific (if nationality is FOREIGNER)
    passport_number: Optional[str] = Field(None, description="Passport number")
    passport_expiry: Optional[str] = Field(None, description="Passport expiry date")
    visa_type: Optional[str] = Field(None, description="Visa type")
    issuing_authority: Optional[str] = Field(None, description="Passport issuing country")
    
    @field_validator('nin')
    def validate_nin(cls, v):
        if v and len(v) != 11:
            raise ValueError('NIN must be 11 digits')
        return v
    
    @field_validator('phone_number')
    def validate_phone(cls, v):
        if v and len(v) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return v


# ============= AUTH MODELS =============
class LoginRequest(BaseModel):
    email: str = Field(..., description="Email or student ID")
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    """Extended registration with Nigerian student data"""
    # Auth credentials
    email: str
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.STUDENT
    
    # Personal Information
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone: Optional[str] = None
    
    # Student Profile (Nigerian-specific)
    profile: Optional[StudentProfile] = None


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    student_id: Optional[str] = None
    is_active: bool = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# ============= DEMO DATABASE =============
DEMO_USERS = {
    "admin@university.edu": {
        "id": "admin-001", "password": "admin123", "first_name": "System",
        "last_name": "Administrator", "role": "admin", "student_id": None
    },
    "student@university.edu": {
        "id": "student-001", "password": "student123", "first_name": "John",
        "last_name": "Doe", "role": "student", "student_id": "UNN/2024/001"
    },
    "lecturer@university.edu": {
        "id": "lecturer-001", "password": "lecturer123", "first_name": "Dr. Sarah",
        "last_name": "Smith", "role": "lecturer", "student_id": None
    },
    "finance@university.edu": {
        "id": "finance-001", "password": "finance123", "first_name": "Mary",
        "last_name": "Johnson", "role": "finance_officer", "student_id": None
    },
}


# ============= HELPER FUNCTIONS =============
def create_token(user_data: dict) -> tuple[str, datetime]:
    expires = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": user_data.get("email"),
        "user_id": user_data.get("id"),
        "role": user_data.get("role"),
        "exp": expires.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, expires


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except:
        return None


# ============= PERMISSIONS =============
ROLE_PERMISSIONS = {
    "admin": ["*"],
    "student": ["courses:read", "grades:read", "finance:read", "profile:write", "enroll:write"],
    "lecturer": ["courses:read", "grades:write", "attendance:write", "timetable:read"],
    "finance_officer": ["finance:read", "finance:write", "students:read"],
    "dean": ["courses:read", "grades:read", "students:read", "reports:read"],
    "hod": ["courses:write", "grades:read", "timetable:write", "students:read"],
    "registrar": ["students:write", "courses:write", "reports:write"],
}


def check_permission(role: str, permission: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, [])
    return "*" in perms or permission in perms


def get_user_from_token(authorization: str = None) -> Optional[dict]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    return decode_token(parts[1])


# ============= EXPORT =============
__all__ = [
    'UserRole', 'LoginRequest', 'RegisterRequest', 'UserResponse',
    'TokenResponse', 'create_token', 'decode_token',
    'get_user_from_token', 'check_permission', 'ROLE_PERMISSIONS',
    'DEMO_USERS'
]