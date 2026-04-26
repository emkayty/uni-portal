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
    # Africa (54 countries)
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", 
    "Central African Republic", "Chad", "Comoros", "Democratic Republic of the Congo", "Republic of the Congo",
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", 
    "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", 
    "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", 
    "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone", 
    "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", 
    "Zimbabwe",
    # Europe (44 countries)
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", 
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", 
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", 
    "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", 
    "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City",
    # Asia (49 countries)
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", 
    "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", 
    "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", 
    "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", 
    "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", 
    "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen",
    # North America
    "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", 
    "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", 
    "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Trinidad and Tobago", "United States",
    # South America
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", 
    "Suriname", "Uruguay", "Venezuela",
    # Oceania
    "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", 
    "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu",
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
# Comprehensive CRUD permissions for university portal
ROLE_PERMISSIONS = {
    # Super Admin - full access
    "admin": ["*"],
    
    # Student - can read own data, register courses
    "student": [
        "courses:read", "grades:read", "finance:read", "profile:read", "profile:write",
        "enroll:write", "enroll:read", "timetable:read", "library:read",
        "transcript:read", "certificates:read", "attendance:read"
    ],
    
    # Lecturer - can manage grades, attendance, view courses
    "lecturer": [
        "courses:read", "courses:write",
        "grades:read", "grades:write", "grades:write:ca", "grades:write:exam",
        "attendance:read", "attendance:write",
        "timetable:read", "timetable:write",
        "students:read", "students:read:own",
        "courses:write:add", "courses:write:remove"
    ],
    
    # HOD (Head of Department) - department management
    "hod": [
        "courses:read", "courses:write", "courses:write:add", "courses:write:remove", "courses:write:edit",
        "grades:read", "grades:write",
        "timetable:read", "timetable:write",
        "students:read", "students:read:department",
        "reports:read", "reports:write",
        "staff:read", "staff:write"
    ],
    
    # Dean - faculty management
    "dean": [
        "courses:read", "courses:write",
        "grades:read", "grades:write",
        "students:read", "students:read:faculty",
        "reports:read", "reports:write",
        "staff:read", "staff:write",
        "curriculum:read", "curriculum:write"
    ],
    
    # Finance Officer - financial operations
    "finance_officer": [
        "finance:read", "finance:write", "finance:write:add", "finance:write:edit",
        "students:read", "students:read:finance",
        "invoices:write", "invoices:write:add", "invoices:write:edit",
        "payments:read", "payments:write",
        "scholarships:read", "scholarships:write",
        "reports:read", "reports:write"
    ],
    
    # Registrar - student records
    "registrar": [
        "students:read", "students:write", "students:write:add", "students:write:edit",
        "students:write:status",
        "courses:read", "courses:write",
        "reports:read", "reports:write",
        "transcript:write", "certificates:write",
        "clearance:write", "clearance:write:department", "clearance:write:final",
        "admission:read", "admission:write"
    ],
    
    # SIWES Coordinator
    "siwes_coordinator": [
        "siwes:read", "siwes:write", "siwes:write:add", "siwes:write:edit",
        "students:read", "companies:read", "companies:write"
    ],
    
    # Exam Officer
    "exam_officer": [
        "exam:read", "exam:write", "exam:write:add", "exam:write:edit",
        "venues:read", "venues:write",
        "invigilators:read", "invigilators:write"
    ],
    
    # Library Officer
    "librarian": [
        "library:read", "library:write", "library:write:add", "library:write:edit",
        "books:read", "books:write", "books:write:add", "books:write:edit",
        "circulation:read", "circulation:write"
    ],
    
    # Alumni Officer
    "alumni_officer": [
        "alumni:read", "alumni:write", "alumni:write:add",
        "students:read", "reports:read"
    ],
}


# Permission helper functions
def check_permission(role: str, permission: str) -> bool:
    """Check if role has specific permission"""
    perms = ROLE_PERMISSIONS.get(role, [])
    return "*" in perms or permission in perms


def check_permission_with_owner(role: str, permission: str, user_id: str, resource_owner_id: str) -> bool:
    """Check permission with owner check (for own records)"""
    if check_permission(role, permission):
        return True
    # Check for own record permission
    if check_permission(role, f"{permission}:own") and user_id == resource_owner_id:
        return True
    return False


def can_read(role: str, resource: str) -> bool:
    """Check if role can read a resource"""
    return check_permission(role, f"{resource}:read") or check_permission(role, f"{resource}:write")


def can_write(role: str, resource: str) -> bool:
    """Check if role can write/edit a resource"""
    return check_permission(role, f"{resource}:write")


def can_add(role: str, resource: str) -> bool:
    """Check if role can add new resource"""
    return check_permission(role, f"{resource}:write:add") or check_permission(role, f"{resource}:write")


def can_delete(role: str, resource: str) -> bool:
    """Check if role can delete a resource (admin only)"""
    return check_permission(role, f"{resource}:write:delete") or "*" in ROLE_PERMISSIONS.get(role, [])


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