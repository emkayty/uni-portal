"""
Authentication Module for University Portal
Provides JWT-based authentication with role-based access control
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

# Fix JWT import for different versions
try:
    import jwt
except ImportError:
    import PyJWT as jwt

from pydantic import BaseModel, Field


# ============= CONSTANTS =============
JWT_SECRET = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


# ============= ENUMS =============
class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    LECTURER = "lecturer"
    FINANCE_OFFICER = "finance_officer"
    DEAN = "dean"
    HOD = "hod"
    REGISTRAR = "registrar"


# ============= MODELS =============
class LoginRequest(BaseModel):
    email: str = Field(..., description="Email or student ID")
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    student_id: Optional[str] = None
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.STUDENT


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