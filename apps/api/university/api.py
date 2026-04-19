"""
University API Endpoints
System-aware endpoints for universities, faculties, departments, programmes
"""
import uuid
from ninja import Router, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

router = Router()


# === SCHEMAS ===

class UniversitySchema(BaseModel):
    id: Optional[str] = None
    name: str
    short_name: str
    code: str
    academic_system: str
    system_type: str
    email: str
    phone: str
    address: str
    nuc_accredited: bool = True
    tetfund_qualified: bool = True
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=str(obj.id) if obj.id else None,
            name=obj.name,
            short_name=obj.short_name,
            code=obj.code,
            academic_system=obj.academic_system,
            system_type=obj.system_type,
            email=obj.email,
            phone=obj.phone,
            address=obj.address,
            nuc_accredited=obj.nuc_accredited,
            tetfund_qualified=obj.tetfund_qualified,
        )


class FacultySchema(BaseModel):
    id: Optional[str] = None
    name: str
    code: str
    university_id: str
    dean: str = ""
    email: str
    
    class Config:
        from_attributes = True


class DepartmentSchema(BaseModel):
    id: Optional[str] = None
    name: str
    code: str
    faculty_id: str
    hod: str = ""
    email: str
    
    class Config:
        from_attributes = True


class ProgrammeSchema(BaseModel):
    id: Optional[str] = None
    name: str
    code: str
    department_id: str
    programme_type: str  # BACHELOR, MASTER, DOCTORATE, ND, HND, BSc, MA, etc.
    duration_years: int = 4
    CCMAS_code: str = ""
    
    class Config:
        from_attributes = True


class SessionSchema(BaseModel):
    id: Optional[str] = None
    session: str  # 2024/2025
    university_id: str
    is_current: bool = False
    start_date: date
    end_date: date
    tuition_fee: float = 0
    
    class Config:
        from_attributes = True


class SemesterSchema(BaseModel):
    id: Optional[str] = None
    name: str  # First, Second, Third
    semester: int  # 1, 2, 3
    session_id: str
    start_date: date
    end_date: date
    
    class Config:
        from_attributes = True


# === ENDPOINTS ===

@router.get("/universities")
def list_universities(
    request,
    type: Optional[str] = Query(None),
    style: Optional[str] = Query(None)
):
    """List all universities with optional filtering"""
    from university.models import University
    queryset = University.objects.all()
    if type:
        queryset = queryset.filter(system_type=type)
    if style:
        queryset = queryset.filter(academic_system=style)
    return [
        {
            "id": str(u.id),
            "name": u.name,
            "short_name": u.short_name,
            "code": u.code,
            "academic_system": u.academic_system,
            "system_type": u.system_type,
            "email": u.email,
            "phone": u.phone,
            "address": u.address,
            "nuc_accredited": u.nuc_accredited,
            "tetfund_qualified": u.tetfund_qualified,
        }
        for u in queryset
    ]


@router.post("/universities")
def create_university(request, data: UniversitySchema):
    """Create a new university"""
    from university.models import University
    uni = University.objects.create(
        name=data.name,
        short_name=data.short_name,
        code=data.code,
        academic_system=data.academic_system,
        system_type=data.system_type,
        email=data.email,
        phone=data.phone,
        address=data.address,
        nuc_accredited=data.nuc_accredited,
        tetfund_qualified=data.tetfund_qualified,
    )
    return uni


@router.get("/universities/{uni_id}")
def get_university(request, uni_id: str):
    """Get university by ID"""
    from university.models import University
    u = University.objects.get(id=uni_id)
    return {
        "id": str(u.id),
        "name": u.name,
        "short_name": u.short_name,
        "code": u.code,
        "academic_system": u.academic_system,
        "system_type": u.system_type,
        "email": u.email,
        "phone": u.phone,
        "address": u.address,
    }


@router.get("/faculties")
def list_faculties(request, university_id: Optional[str] = Query(None)):
    """List faculties"""
    from university.models import Faculty
    queryset = Faculty.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    return [
        {"id": str(f.id), "name": f.name, "code": f.code, "university": f.university.short_name, "dean": f.dean, "email": f.email}
        for f in queryset
    ]


@router.post("/faculties")
def create_faculty(request, data: FacultySchema):
    """Create a new faculty"""
    from university.models import Faculty, University
    uni = University.objects.get(id=data.university_id)
    fac = Faculty.objects.create(
        university=uni,
        name=data.name,
        code=data.code,
        dean=data.dean,
        email=data.email,
    )
    return fac


@router.get("/departments")
def list_departments(request, faculty_id: Optional[str] = Query(None)):
    """List departments"""
    from university.models import Department
    queryset = Department.objects.all()
    if faculty_id:
        queryset = queryset.filter(faculty_id=faculty_id)
    return[{"id":str(q.id),"name":q.name,"code":q.code}for q in queryset]


@router.post("/departments")
def create_department(request, data: DepartmentSchema):
    """Create a new department"""
    from university.models import Department, Faculty
    fac = Faculty.objects.get(id=data.faculty_id)
    dept = Department.objects.create(
        faculty=fac,
        name=data.name,
        code=data.code,
        hod=data.hod,
        email=data.email,
    )
    return dept


@router.get("/programmes")
def list_programmes(request, 
    department_id: Optional[str] = Query(None),
    programme_type: Optional[str] = Query(None)
):
    """List programmes"""
    from university.models import Programme
    queryset = Programme.objects.all()
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    if programme_type:
        queryset = queryset.filter(programme_type=programme_type)
    return[{"id":str(q.id),"name":q.name,"code":q.code}for q in queryset]


@router.post("/programmes")
def create_programme(request, data: ProgrammeSchema):
    """Create a new programme"""
    from university.models import Programme, Department
    dept = Department.objects.get(id=data.department_id)
    prog = Programme.objects.create(
        department=dept,
        name=data.name,
        code=data.code,
        programme_type=data.programme_type,
        duration_years=data.duration_years,
        CCMAS_code=data.CCMAS_code,
    )
    return prog


@router.get("/sessions")
def list_sessions(request, university_id: Optional[str] = Query(None)):
    """List academic sessions"""
    from university.models import Session
    queryset = Session.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    return [
        {
            "id": str(s.id),
            "session": s.session,
            "university": s.university.short_name,
            "is_current": s.is_current,
            "start_date": str(s.start_date) if s.start_date else None,
            "end_date": str(s.end_date) if s.end_date else None,
            "tuition_fee": float(s.tuition_fee) if s.tuition_fee else 0,
        }
        for s in queryset
    ]


@router.post("/sessions")
def create_session(request, data: SessionSchema):
    """Create a new academic session"""
    from university.models import Session, University
    uni = University.objects.get(id=data.university_id)
    session = Session.objects.create(
        university=uni,
        session=data.session,
        is_current=data.is_current,
        start_date=data.start_date,
        end_date=data.end_date,
        tuition_fee=data.tuition_fee,
    )
    return session


@router.get("/semesters")
def list_semesters(request, session_id: Optional[str] = Query(None)):
    """List semesters"""
    from university.models import Semester
    queryset = Semester.objects.all()
    if session_id:
        queryset = queryset.filter(session_id=session_id)
    return[{"id":str(q.id),"name":q.name,"code":q.code}for q in queryset]


@router.post("/semesters")
def create_semester(request, data: SemesterSchema):
    """Create a new semester"""
    from university.models import Semester, Session
    session = Session.objects.get(id=data.session_id)
    sem = Semester.objects.create(
        session=session,
        name=data.name,
        semester=data.semester,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    return sem


@router.get("/grading-config/{uni_id}")
def get_grading_config(request, uni_id: str):
    """Get grading configuration for a university"""
    from university.models import University
    uni = University.objects.get(id=uni_id)
    return {
        "university": uni.short_name,
        "academic_system": uni.academic_system,
        "grading_scale": uni.get_grading_config()
    }