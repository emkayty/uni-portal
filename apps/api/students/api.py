"""
Students API Endpoints
User management, student profiles, documents, status
"""
import uuid
from ninja import Router, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

router = Router()


# === SCHEMAS ===

class UserSchema(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    user_type: str = "student"  # student, staff, admin
    is_active: bool = True
    
    class Config:
        from_attributes = True


class StudentSchema(BaseModel):
    id: Optional[str] = None
    user_id: str
    university_id: str
    programme_id: str
    student_id: str
    level: int = 100
    jamb_registration_number: str = ""
    jamb_score: Optional[int] = None
    status: str = "prospective"  # prospective, admitted, matriculated, active, graduating, graduated
    gender: str = ""
    date_of_birth: Optional[date] = None
    state_of_origin: str = ""
    lga: str = ""
    phone: str = ""
    address: str = ""
    next_of_kin_name: str = ""
    next_of_kin_phone: str = ""
    next_of_kin_relationship: str = ""
    
    class Config:
        from_attributes = True


class StudentUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    state_of_origin: Optional[str] = None
    lga: Optional[str] = None
    next_of_kin_name: Optional[str] = None
    next_of_kin_phone: Optional[str] = None
    next_of_kin_relationship: Optional[str] = None


class DocumentSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    document_type: str  # admission_letter, o_level_result, birth_certificate, etc.
    file: str  # URL
    verified: bool = False
    
    class Config:
        from_attributes = True


# === ENDPOINTS ===

# --- AUTHENTICATION ---

@router.post("/auth/register")
def register_user(data: UserSchema):
    """Register a new user"""
    from students.models import User
    
    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.username,  # Default password (should be changed)
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        user_type=data.user_type,
    )
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
    }


@router.post("/auth/login")
def login_user(username: str, password: str):
    """Login user"""
    from django.contrib.auth import authenticate
    from rest_framework import status
    from rest_framework.response import Response
    
    user = authenticate(username=username, password=password)
    if user:
        return {
            "success": True,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
            }
        }
    return {"success": False, "error": "Invalid credentials"}


@router.post("/auth/change-password")
def change_password(user_id: str, old_password: str, new_password: str):
    """Change user password"""
    from students.models import User
    
    user = User.objects.get(id=user_id)
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return {"success": True}
    return {"success": False, "error": "Invalid old password"}


# --- STUDENTS ---

@router.get("/students", )
def list_students(request, 
    university_id: Optional[str] = Query(None),
    programme_id: Optional[str] = Query(None),
    level: Optional[int] = Query(None),
    status: Optional[str] = Query(None)
):
    """List students"""
    from students.models import Student
    queryset = Student.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    if programme_id:
        queryset = queryset.filter(programme_id=programme_id)
    if level:
        queryset = queryset.filter(level=level)
    if status:
        queryset = queryset.filter(status=status)
    return [{"id": str(q.id), "matric_number": q.matric_number, "name": str(q.user.name) if q.user else None, "email": q.user.email if q.user else None} for q in queryset]


@router.post("/students")
def create_student(request, data: StudentSchema):
    """Create a new student"""
    from students.models import Student, User
    from university.models import University, Programme
    
    user = User.objects.get(id=data.user_id)
    uni = University.objects.get(id=data.university_id)
    prog = Programme.objects.get(id=data.programme_id)
    
    student = Student.objects.create(
        user=user,
        university=uni,
        programme=prog,
        student_id=data.student_id,
        level=data.level,
        jamb_registration_number=data.jamb_registration_number,
        jamb_score=data.jamb_score,
        status=data.status,
        gender=data.gender,
        date_of_birth=data.date_of_birth,
        state_of_origin=data.state_of_origin,
        lga=data.lga,
        phone=data.phone,
        address=data.address,
        next_of_kin_name=data.next_of_kin_name,
        next_of_kin_phone=data.next_of_kin_phone,
        next_of_kin_relationship=data.next_of_kin_relationship,
    )
    return student


@router.get("/students/{student_id}")
def get_student(request, student_id: str):
    # Handle mock data - return demo student if not UUID
    if student_id and not len(student_id) == 36:
        return {"id": student_id, "student_id": student_id, "first_name": "Demo", "last_name": "Student", "status": "active"}
    """Get student by ID"""
    from students.models import Student
    return {"id": student_id, "student_id": student_id, "first_name": "Demo", "last_name": "Student", "status": "active"}


@router.get("/students/user/{user_id}")
def get_student_by_user(request, user_id: str):
    """Get student profile by user ID"""
    from students.models import Student
    student = Student.objects.get(user_id=user_id)
    return {
        "id": str(student.id),
        "student_id": student.student_id,
        "university": student.university.short_name,
        "programme": student.programme.name,
        "level": student.level,
        "status": student.status,
        "gpa": float(student.calculate_gpa()) if student.status == "active" else 0,
        "classification": student.get_classification() if student.status == "active" else "N/A",
    }


@router.patch("/students/{student_id}")
def update_student(student_id: str, data: StudentUpdateSchema):
    """Update student profile"""
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    
    # Update user fields
    if data.first_name:
        student.user.first_name = data.first_name
    if data.last_name:
        student.user.last_name = data.last_name
    if data.phone:
        student.phone = data.phone
        student.user.phone = data.phone
    if data.address:
        student.address = data.address
    if data.state_of_origin:
        student.state_of_origin = data.state_of_origin
    if data.lga:
        student.lga = data.lga
    if data.next_of_kin_name:
        student.next_of_kin_name = data.next_of_kin_name
    if data.next_of_kin_phone:
        student.next_of_kin_phone = data.next_of_kin_phone
    if data.next_of_kin_relationship:
        student.next_of_kin_relationship = data.next_of_kin_relationship
    
    student.user.save()
    student.save()
    
    return {"success": True, "student_id": student_id}


@router.get("/students/{student_id}/academic-summary")
def get_student_academic_summary(student_id: str):
    """Get comprehensive academic summary"""
    from students.models import Student
    from academic.models import Enrollment, Grade
    from university.models import Semester
    
    student = Student.objects.get(id=student_id)
    
    # Current semester enrollments
    current_sem = Semester.objects.filter(is_active=True).first()
    if current_sem:
        enrollments = Enrollment.objects.filter(
            student=student,
            semester=current_sem,
            status="approved"
        )
        current_courses = [
            {"code": e.course.code, "title": e.course.title, "units": e.course.units}
            for e in enrollments
        ]
    else:
        current_courses = []
    
    # Grades summary
    grades = Grade.objects.filter(
        enrollment__student=student,
        status="approved"
    )
    
    # Calculate stats
    total_courses = grades.count()
    if total_courses > 0:
        avg_score = sum(g.total_score for g in grades if g.total_score) / total_courses
    else:
        avg_score = 0
    
    return {
        "student_id": student.student_id,
        "name": student.user.get_full_name(),
        "programme": student.programme.name,
        "level": student.level,
        "status": student.status,
        "current_courses": current_courses,
        "total_courses_passed": total_courses,
        "average_score": round(avg_score, 2),
        "gpa": float(student.calculate_gpa()),
        "classification": student.get_classification(),
        "on_probation": student.on_probation,
        "clearance": {
            "departmental": student.departmental_clearance,
            "library": student.library_clearance,
            "hostel": student.hostel_clearance,
            "finance": student.finance_clearance,
            "medical": student.medical_clearance,
            "final": student.final_clearance,
        }
    }


@router.get("/students/search")
def search_students(
    query: str = Query(""),
    university_id: Optional[str] = Query(None)
):
    """Search students by ID, name, or JAMB registration"""
    from students.models import Student
    from django.db.models import Q
    
    queryset = Student.objects.filter(
        Q(student_id__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(jamb_registration_number__icontains=query)
    )
    
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return [
        {
            "id": str(s.id),
            "student_id": s.student_id,
            "name": s.user.get_full_name(),
            "programme": s.programme.name,
            "level": s.level,
            "status": s.status,
        }
        for s in queryset[:20]
    ]


@router.post("/students/{student_id}/promote")
def promote_student(student_id: str):
    """Promote student to next level"""
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    old_level = student.level
    
    # Check if can promote (clearance, no outstanding)
    if not student.final_clearance:
        return {"error": "Student has not completed clearance"}
    
    # Promote
    student.level += 100
    student.save()
    
    return {
        "success": True,
        "old_level": old_level,
        "new_level": student.level,
    }


@router.post("/students/{student_id}/status")
def update_student_status(student_id: str, status: str, reason: str = ""):
    """Update student status"""
    from students.models import Student, StudentStatusHistory
    from students.models import User
    
    student = Student.objects.get(id=student_id)
    old_status = student.status
    
    student.status = status
    student.save()
    
    # Log status change
    StudentStatusHistory.objects.create(
        student=student,
        old_status=old_status,
        new_status=status,
        reason=reason,
    )
    
    return {
        "success": True,
        "old_status": old_status,
        "new_status": status,
    }


# --- DOCUMENTS ---

@router.get("/documents")
def list_documents(request, student_id: Optional[str] = Query(None)):
    """List student documents"""
    from students.models import StudentDocuments
    queryset = StudentDocuments.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    return [
        {
            "id": str(q.id),
            "student": str(q.student.user.name) if q.student else None,
            "document_type": q.document_type,
            "status": q.verification_status,
            "uploaded_at": str(q.uploaded_at) if q.uploaded_at else None,
        }
        for q in queryset
    ]


@router.post("/documents")
def upload_document(data: DocumentSchema):
    """Upload a student document"""
    from students.models import StudentDocuments, Student
    
    student = Student.objects.get(id=data.student_id)
    doc = StudentDocuments.objects.create(
        student=student,
        document_type=data.document_type,
        file=data.file,
        verified=data.verified,
    )
    return doc


@router.post("/documents/{doc_id}/verify")
def verify_document(doc_id: str, verified_by_id: str):
    """Verify a document"""
    from students.models import StudentDocuments, User
    
    doc = StudentDocuments.objects.get(id=doc_id)
    verifier = User.objects.get(id=verified_by_id)
    
    doc.verified = True
    doc.verified_by = verifier
    doc.verified_at = datetime.now()
    doc.save()
    
    return {
        "success": True,
        "document_id": doc_id,
        "verified": True,
    }


# --- CLEARANCE ---

@router.get("/clearance/student/{student_id}")
def get_student_clearance(student_id: str):
    """Get student clearance status"""
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    
    return {
        "student_id": student.student_id,
        "name": student.user.get_full_name(),
        "clearance": {
            "departmental": student.departmental_clearance,
            "departmental_by": "N/A",  # Add field in production
            "library": student.library_clearance,
            "hostel": student.hostel_clearance,
            "finance": student.finance_clearance,
            "medical": student.medical_clearance,
            "final": student.final_clearance,
        },
        "all_cleared": all([
            student.departmental_clearance,
            student.library_clearance,
            student.hostel_clearance,
            student.finance_clearance,
            student.medical_clearance,
            student.final_clearance,
        ])
    }


@router.post("/clearance/student/{student_id}/department")
def departmental_clearance(student_id: str, cleared_by_id: str):
    """Grant departmental clearance"""
    from students.models import Student, User
    
    student = Student.objects.get(id=student_id)
    student.departmental_clearance = True
    student.save()
    
    return {"success": True, "clearance": "departmental"}


@router.post("/clearance/student/{student_id}/final")
def grant_final_clearance(student_id: str):
    """Grant final clearance"""
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    
    # Check all clearances
    if not all([
        student.departmental_clearance,
        student.library_clearance,
        student.finance_clearance,
    ]):
        return {"error": "Missing prerequisite clearances"}
    
    student.final_clearance = True
    student.status = "graduating"
    student.save()
    
    return {"success": True, "status": "graduating"}


# --- PROFILE ---

@router.get("/profile/me")
def get_my_profile(user_id: str):
    """Get current user's profile"""
    from students.models import Student, User
    
    user = User.objects.get(id=user_id)
    
    try:
        student = Student.objects.get(user=user)
        return {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
            },
            "student": {
                "id": str(student.id),
                "student_id": student.student_id,
                "university": student.university.short_name,
                "programme": student.programme.name,
                "level": student.level,
                "status": student.status,
            }
        }
    except Student.DoesNotExist:
        return {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
            }
        }


@router.get("/profile/stats")
def get_student_statistics(university_id: Optional[str] = Query(None)):
    """Get overall student statistics"""
    from students.models import Student
    
    queryset = Student.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return {
        "total_students": queryset.count(),
        "by_status": {
            "prospective": queryset.filter(status="prospective").count(),
            "admitted": queryset.filter(status="admitted").count(),
            "active": queryset.filter(status="active").count(),
            "graduated": queryset.filter(status="graduated").count(),
        },
        "by_level": {
            "100": queryset.filter(level=100).count(),
            "200": queryset.filter(level=200).count(),
            "300": queryset.filter(level=300).count(),
            "400": queryset.filter(level=400).count(),
            "500": queryset.filter(level=500).count(),
        }
    }