"""
Academic API Endpoints
Courses, enrollments, grades, timetables, venues, hostels
"""
import uuid
from ninja import Router, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import time

router = Router()


# === SCHEMAS ===

class CourseSchema(BaseModel):
    id: Optional[str] = None
    code: str
    title: str
    university_id: str
    department_id: str
    units: int = 3
    level: int = 100  # 100, 200, 300, 400, 500
    course_type: str = "core"  # core, elective, general
    semester_offered: str = ""  # First, Second, Both
    max_capacity: int = 500
    ca_weight: float = 30.0
    exam_weight: float = 70.0
    CCMAS_code: str = ""
    
    class Config:
        from_attributes = True


class EnrollmentSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    course_id: str
    semester_id: str
    status: str = "pending"  # pending, approved, dropped
    grade: str = ""
    grade_points: Optional[float] = None
    
    class Config:
        from_attributes = True


class GradeSchema(BaseModel):
    id: Optional[str] = None
    enrollment_id: str
    ca_score: Optional[float] = None
    midterm_score: Optional[float] = None
    exam_score: Optional[float] = None
    total_score: Optional[float] = None
    grade: str = ""
    grade_points: Optional[float] = None
    status: str = "pending"  # pending, submitted, approved
    
    class Config:
        from_attributes = True


# ============= COURSE REGISTRATION =============

class CourseRegistrationRequest(BaseModel):
    student_id: str
    semester_id: str
    course_ids: List[str] = Field(..., description="List of course IDs to register")


class EnrollmentApprovalRequest(BaseModel):
    enrollment_ids: List[str]
    action: str = Field(..., description="approve or reject")


class GradeSubmissionRequest(BaseModel):
    enrollment_id: str
    ca_score: float = Field(..., ge=0, le=100)
    exam_score: float = Field(..., ge=0, le=100)


class AttendanceRecord(BaseModel):
    student_id: str
    course_id: str
    date: str
    status: str = "present"  # present, absent, late


# ============= IN-MEMORY STORAGE =============
# Demo storage for course registrations
ENROLLMENT_STORAGE = []


@router.post("/enrollments/register")
def register_courses(request, data: CourseRegistrationRequest):
    """Register student for courses in a semester"""
    results = []
    for course_id in data.course_ids:
        enrollment = {
            "id": f"enroll-{len(ENROLLMENT_STORAGE)+1}",
            "student_id": data.student_id,
            "course_id": course_id,
            "semester_id": data.semester_id,
            "status": "pending",
            "created_at": "2024-01-15"
        }
        ENROLLMENT_STORAGE.append(enrollment)
        results.append(enrollment)
    return {
        "success": True,
        "message": f"Registered for {len(results)} courses",
        "enrollments": results
    }


@router.post("/enrollments/approve")
def approve_enrollments(request, data: EnrollmentApprovalRequest):
    """Approve or reject enrollments"""
    results = []
    for enroll in ENROLLMENT_STORAGE:
        if enroll["id"] in data.enrollment_ids:
            enroll["status"] = "approved" if data.action == "approve" else "rejected"
            results.append(enroll)
    return {
        "success": True,
        "message": f"{data.action.title()}d {len(results)} enrollments",
        "enrollments": results
    }


@router.post("/grades/submit")
def submit_grade(request, data: GradeSubmissionRequest):
    """Submit grade for an enrollment"""
    # Calculate total and grade
    total = (data.ca_score * 0.3) + (data.exam_score * 0.7)
    
    # Determine letter grade
    if total >= 70: grade, points = "A", 5.0
    elif total >= 60: grade, points = "B", 4.0
    elif total >= 50: grade, points = "C", 3.0
    elif total >= 45: grade, points = "D", 2.0
    else: grade, points = "F", 0.0
    
    return {
        "success": True,
        "message": "Grade submitted",
        "grade": {
            "enrollment_id": data.enrollment_id,
            "ca_score": data.ca_score,
            "exam_score": data.exam_score,
            "total_score": round(total, 2),
            "grade": grade,
            "grade_points": points,
            "status": "submitted"
        }
    }


@router.get("/grades/calculate-gpa/{student_id}")
def calculate_gpa(request, student_id: str):
    """Calculate student's GPA"""
    # Demo grades
    grades = [
        {"course": "CSC101", "units": 3, "points": 4.0},
        {"course": "MTH101", "units": 3, "points": 5.0},
        {"course": "PHY101", "units": 4, "points": 4.0},
    ]
    
    total_points = sum(g["units"] * g["points"] for g in grades)
    total_units = sum(g["units"] for g in grades)
    gpa = round(total_points / total_units, 2) if total_units > 0 else 0
    
    return {
        "student_id": student_id,
        "gpa": gpa,
        "total_units": total_units,
        "courses": grades
    }


# ============= ATTENDANCE =============
ATTENDANCE_STORAGE = []


@router.post("/attendance/mark")
def mark_attendance(request, data: AttendanceRecord):
    """Mark student attendance"""
    record = {
        "id": f"att-{len(ATTENDANCE_STORAGE)+1}",
        "student_id": data.student_id,
        "course_id": data.course_id,
        "date": data.date,
        "status": data.status
    }
    ATTENDANCE_STORAGE.append(record)
    return {"success": True, "record": record}


@router.get("/attendance/{student_id}")
def get_attendance(request, student_id: str):
    """Get student's attendance records"""
    records = [r for r in ATTENDANCE_STORAGE if r["student_id"] == student_id]
    return {"student_id": student_id, "attendance": records}


@router.get("/attendance/{student_id}/summary")
def get_attendance_summary(request, student_id: str):
    """Get attendance percentage summary"""
    records = [r for r in ATTENDANCE_STORAGE if r["student_id"] == student_id]
    if not records:
        return {"student_id": student_id, "attendance_rate": 100.0, "total": 0}
    
    present = sum(1 for r in records if r["status"] == "present")
    rate = round((present / len(records)) * 100, 1)
    return {"student_id": student_id, "attendance_rate": rate, "total": len(records)}


# ============= DEGREE AUDIT =============

@router.get("/degree-audit/{student_id}")
def degree_audit(request, student_id: str):
    """Check degree progress and graduation eligibility"""
    # Demo data
    completed_courses = [
        {"code": "CSC101", "title": "Intro to Computing", "units": 3, "grade": "A", "level": 100},
        {"code": "MTH101", "title": "Calculus I", "units": 3, "grade": "B", "level": 100},
        {"code": "PHY101", "title": "Physics I", "units": 4, "grade": "A", "level": 100},
        {"code": "CSC201", "title": "Data Structures", "units": 3, "grade": "A", "level": 200},
    ]
    
    required_units = 120
    earned_units = sum(c["units"] for c in completed_courses)
    gpa = 4.2
    
    # Requirements for Nigerian universities
    required_courses = ["CSC101", "MTH101", "PHY101", "CSC201", "CSC301", "CSC401"]
    completed_codes = [c["code"] for c in completed_courses]
    missing = [r for r in required_courses if r not in completed_codes]
    
    return {
        "student_id": student_id,
        "degree": "B.Sc. Computer Science",
        "total_required": required_units,
        "units_earned": earned_units,
        "units_remaining": required_units - earned_units,
        "gpa": gpa,
        "graduation_eligible": earned_units >= required_units and gpa >= 2.0,
        "completed_courses": completed_courses,
        "missing_courses": missing,
        "progress_percent": round((earned_units / required_units) * 100, 1)
    }


class TimetableSchema(BaseModel):
    id: Optional[str] = None
    course_id: str
    semester_id: str
    venue_id: str
    day: str  # monday, tuesday, etc.
    start_time: str  # "HH:MM"
    end_time: str
    lecturer_id: Optional[str] = None
    section: str = ""
    
    class Config:
        from_attributes = True


class VenueSchema(BaseModel):
    id: Optional[str] = None
    name: str
    building: str
    university_id: str
    venue_type: str = "lecture_hall"
    capacity: int
    exam_capacity: int = 0
    
    class Config:
        from_attributes = True


class HostelSchema(BaseModel):
    id: Optional[str] = None
    name: str
    code: str
    university_id: str
    gender: str  # Male, Female, Mixed
    total_beds: int
    occupied_beds: int = 0
    warden: str = ""
    contact: str = ""
    
    class Config:
        from_attributes = True


class HostelApplicationSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    semester_id: str
    first_choice_id: Optional[str] = None
    second_choice_id: Optional[str] = None
    status: str = "pending"  # pending, approved, rejected, allocated
    allocated_hostel_id: Optional[str] = None
    room_number: str = ""
    bed_number: str = ""
    
    class Config:
        from_attributes = True


class ExamSittingSchema(BaseModel):
    id: Optional[str] = None
    course_id: str
    semester_id: str
    venue_id: str
    date: str
    start_time: str
    end_time: str
    invigilator_id: Optional[str] = None
    
    class Config:
        from_attributes = True


# === ENDPOINTS ===

# --- COURSES ---

@router.get("/courses")
def list_courses(request, 
    department_id: Optional[str] = Query(None),
    level: Optional[int] = Query(None),
    semester: Optional[str] = Query(None)
):
    """List courses"""
    from academic.models import Course
    queryset = Course.objects.all()
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    if level:
        queryset = queryset.filter(level=level)
    if semester:
        queryset = queryset.filter(semester_offered__icontains=semester)
    return [
        {
            "id": str(c.id),
            "code": c.code,
            "title": c.title,
            "department": c.department.name if c.department else None,
            "level": c.level,
            "units": c.units,
            "semester": c.semester_offered,
        }
        for c in queryset
    ]


@router.post("/courses")
def create_course(request, data: CourseSchema):
    """Create a new course"""
    from academic.models import Course, University, Department
    uni = University.objects.get(id=data.university_id)
    dept = Department.objects.get(id=data.department_id)
    course = Course.objects.create(
        university=uni,
        department=dept,
        code=data.code,
        title=data.title,
        units=data.units,
        level=data.level,
        course_type=data.course_type,
        semester_offered=data.semester_offered,
        max_capacity=data.max_capacity,
        ca_weight=data.ca_weight,
        exam_weight=data.exam_weight,
        CCMAS_code=data.CCMAS_code,
    )
    return course


@router.get("/courses/{course_id}")
def get_course(request, course_id: str):
    """Get course by ID"""
    from academic.models import Course
    c=Course.objects.get(id=course_id);return{"id":str(c.id),"code":c.code,"title":c.title}


@router.get("/courses/{course_id}/students")
def get_course_students(request, course_id: str):
    """Get students enrolled in a course"""
    from academic.models import Course, Enrollment
    course = Course.objects.get(id=course_id)
    enrollments = Enrollment.objects.filter(course=course, status="approved")
    return {
        "course": course.code,
        "title": course.title,
        "enrolled": enrollments.count(),
        "students": [
            {"id": e.student.student_id, "name": e.student.user.get_full_name()}
            for e in enrollments
        ]
    }


# --- ENROLLMENTS ---

@router.get("/enrollments")
def list_enrollments(request, 
    student_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None),
    semester_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List enrollments"""
    from academic.models import Enrollment
    queryset = Enrollment.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    if semester_id:
        queryset = queryset.filter(semester_id=semester_id)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(e.id),
            "student": str(e.student.user.name) if e.student else None,
            "course": e.course.code if e.course else None,
            "semester": e.semester.name if e.semester else None,
            "status": e.status,
            "enrolled_at": str(e.enrolled_at) if e.enrolled_at else None,
        }
        for e in queryset
    ]


@router.post("/enrollments")
def create_enrollment(request, data: EnrollmentSchema):
    """Create a new enrollment (course registration)"""
    from academic.models import Enrollment, students, Course, Semester
    student = students.Student.objects.get(id=data.student_id)
    course = Course.objects.get(id=data.course_id)
    semester = Semester.objects.get(id=data.semester_id)
    
    # Check for prerequisites (simplified)
    if course.prerequisite_courses:
        # In production, validate prerequisites
        pass
    
    enrollment = Enrollment.objects.create(
        student=student,
        course=course,
        semester=semester,
        status=data.status,
    )
    return enrollment


@router.post("/enrollments/{enrollment_id}/approve")
def approve_enrollment(enrollment_id: str):
    """Approve an enrollment"""
    from academic.models import Enrollment
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollment.status = "approved"
    enrollment.save()
    return {"status": "approved", "enrollment_id": enrollment_id}


@router.post("/enrollments/{enrollment_id}/drop")
def drop_enrollment(enrollment_id: str, reason: str = ""):
    """Drop an enrollment"""
    from academic.models import Enrollment
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollment.status = "dropped"
    enrollment.drop_reason = reason
    enrollment.save()
    return {"status": "dropped", "enrollment_id": enrollment_id}


# --- GRADES ---

@router.get("/grades", )
def list_grades(request, 
    student_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None),
    semester_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List grades"""
    from academic.models import Grade, Enrollment
    queryset = Grade.objects.all()
    if student_id:
        queryset = queryset.filter(enrollment__student_id=student_id)
    if course_id:
        queryset = queryset.filter(enrollment__course_id=course_id)
    if semester_id:
        queryset = queryset.filter(enrollment__semester_id=semester_id)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(g.id),
            "student": str(g.enrollment.student.user.name) if g.enrollment and g.enrollment.student else None,
            "course": g.enrollment.course.code if g.enrollment and g.enrollment.course else None,
            "score": g.score,
            "grade": g.grade,
            "points": g.points,
            "status": g.status,
        }
        for g in queryset
    ]


@router.post("/grades")
def create_grade(request, data: GradeSchema):
    """Enter grades for a student"""
    from academic.models import Grade, Enrollment
    enrollment = Enrollment.objects.get(id=data.enrollment_id)
    
    grade = Grade.objects.create(
        enrollment=enrollment,
        ca_score=data.ca_score,
        midterm_score=data.midterm_score,
        exam_score=data.exam_score,
        total_score=data.total_score,
        grade=data.grade,
        grade_points=data.grade_points,
        status=data.status,
    )
    return grade


@router.get("/grades/student/{student_id}/semester/{semester_id}")
def get_student_semester_grades(student_id: str, semester_id: str):
    """Get student's grades for a semester"""
    from academic.models import Grade, Enrollment
    
    enrollments = Enrollment.objects.filter(
        student_id=student_id,
        semester_id=semester_id,
        status="approved"
    )
    
    results = []
    total_points = 0
    total_units = 0
    
    for e in enrollments:
        try:
            g = e.grade_record
            results.append({
                "course": e.course.code,
                "title": e.course.title,
                "units": e.course.units,
                "score": g.total_score,
                "grade": g.grade,
                "points": g.grade_points,
            })
            if g.grade_points and e.course.units:
                total_points += g.grade_points * e.course.units
                total_units += e.course.units
        except:
            results.append({
                "course": e.course.code,
                "title": e.course.title,
                "units": e.course.units,
                "score": None,
                "grade": "N/A",
                "points": None,
            })
    
    gpa = round(total_points / total_units, 2) if total_units > 0 else 0
    
    return {
        "semester": semester_id,
        "courses": results,
        "total_units": total_units,
        "gpa": gpa
    }


# --- TIMETABLES ---

@router.get("/timetables", )
def list_timetables(request, 
    course_id: Optional[str] = Query(None),
    semester_id: Optional[str] = Query(None),
    day: Optional[str] = Query(None)
):
    """List timetables"""
    from academic.models import Timetable
    queryset = Timetable.objects.all()
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    if semester_id:
        queryset = queryset.filter(semester_id=semester_id)
    if day:
        queryset = queryset.filter(day=day)
    return [
        {
            "id": str(t.id),
            "course": t.course.code if t.course else None,
            "venue": t.venue.name if t.venue else None,
            "day": t.day,
            "start_time": t.start_time,
            "end_time": t.end_time,
        }
        for t in queryset
    ]


@router.post("/timetables")
def create_timetable(request, data: TimetableSchema):
    """Create a timetable entry"""
    from academic.models import Timetable, Course, Semester, Venue
    from students.models import User
    
    course = Course.objects.get(id=data.course_id)
    semester = Semester.objects.get(id=data.semester_id)
    venue = Venue.objects.get(id=data.venue_id)
    
    lecturer = None
    if data.lecturer_id:
        try:
            lecturer = User.objects.get(id=data.lecturer_id, user_type='staff')
        except:
            pass
    
    tt = Timetable.objects.create(
        course=course,
        semester=semester,
        venue=venue,
        day=data.day,
        start_time=data.start_time,
        end_time=data.end_time,
        lecturer=lecturer,
        section=data.section,
    )
    return tt


@router.get("/timetables/student/{student_id}/semester/{semester_id}")
def get_student_timetable(student_id: str, semester_id: str):
    """Get student's timetable for a semester"""
    from academic.models import Timetable, Enrollment
    
    enrollments = Enrollment.objects.filter(
        student_id=student_id,
        semester_id=semester_id,
        status="approved"
    )
    
    course_ids = [e.course_id for e in enrollments]
    timetables = Timetable.objects.filter(
        course_id__in=course_ids,
        semester_id=semester_id
    ).order_by('day', 'start_time')
    
    schedule = {}
    for tt in timetables:
        day = tt.day
        if day not in schedule:
            schedule[day] = []
        schedule[day].append({
            "time": f"{tt.start_time}-{tt.end_time}",
            "course": tt.course.code,
            "title": tt.course.title,
            "venue": tt.venue.name,
        })
    
    return schedule


# --- VENUES ---

@router.get("/venues", )
def list_venues(request, 
    university_id: Optional[str] = Query(None),
    venue_type: Optional[str] = Query(None)
):
    """List venues"""
    from academic.models import Venue
    queryset = Venue.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    if venue_type:
        queryset = queryset.filter(venue_type=venue_type)
    return [
        {
            "id": str(v.id),
            "name": v.name,
            "building": v.building,
            "capacity": v.capacity,
            "type": v.venue_type,
        }
        for v in queryset
    ]


@router.post("/venues")
def create_venue(request, data: VenueSchema):
    """Create a new venue"""
    from academic.models import Venue, University
    uni = University.objects.get(id=data.university_id)
    venue = Venue.objects.create(
        university=uni,
        name=data.name,
        building=data.building,
        venue_type=data.venue_type,
        capacity=data.capacity,
        exam_capacity=data.exam_capacity,
    )
    return venue


# --- HOSTELS ---

@router.get("/hostels", )
def list_hostels(request, 
    university_id: Optional[str] = Query(None),
    gender: Optional[str] = Query(None)
):
    """List hostels"""
    from academic.models import Hostel
    queryset = Hostel.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    if gender:
        queryset = queryset.filter(gender=gender)
    return [
        {
            "id": str(h.id),
            "name": h.name,
            "gender": h.gender,
            "total_beds": h.total_beds,
            "occupied_beds": h.occupied_beds,
            "available": h.total_beds - h.occupied_beds,
        }
        for h in queryset
    ]


@router.post("/hostels")
def create_hostel(request, data: HostelSchema):
    """Create a new hostel"""
    from academic.models import Hostel, University
    uni = University.objects.get(id=data.university_id)
    hostel = Hostel.objects.create(
        university=uni,
        name=data.name,
        code=data.code,
        gender=data.gender,
        total_beds=data.total_beds,
        warden=data.warden,
        contact=data.contact,
    )
    return hostel


@router.get("/hostels/available")
def get_available_hostels(
    university_id: str,
    gender: str
):
    """Get available hostels with beds"""
    from academic.models import Hostel
    hostels = Hostel.objects.filter(
        university_id=university_id,
        gender=gender,
        is_active=True
    )
    return [
        {
            "id": h.id,
            "name": h.name,
            "code": h.code,
            "total_beds": h.total_beds,
            "occupied_beds": h.occupied_beds,
            "available": h.total_beds - h.occupied_beds,
        }
        for h in hostels
    ]


# --- HOSTEL APPLICATIONS ---

@router.get("/hostel-applications", )
def list_hostel_applications(
    student_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List hostel applications"""
    from academic.models import HostelApplication
    queryset = HostelApplication.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if status:
        queryset = queryset.filter(status=status)
    return queryset


@router.post("/hostel-applications")
def create_hostel_application(request, data: HostelApplicationSchema):
    """Apply for hostel accommodation"""
    from academic.models import HostelApplication, Hostel
    from students.models import Student, Semester
    
    student = Student.objects.get(id=data.student_id)
    semester = Semester.objects.get(id=data.semester_id)
    
    first_choice = None
    if data.first_choice_id:
        first_choice = Hostel.objects.get(id=data.first_choice_id)
    
    second_choice = None
    if data.second_choice_id:
        second_choice = Hostel.objects.get(id=data.second_choice_id)
    
    app = HostelApplication.objects.create(
        student=student,
        semester=semester,
        first_choice=first_choice,
        second_choice=second_choice,
        status=data.status,
    )
    return app


@router.post("/hostel-applications/{app_id}/allocate")
def allocate_hostel(app_id: str, hostel_id: str, room: str, bed: str):
    """Allocate hostel to a student"""
    from academic.models import HostelApplication, Hostel
    
    app = HostelApplication.objects.get(id=app_id)
    hostel = Hostel.objects.get(id=hostel_id)
    
    app.allocated_hostel = hostel
    app.room_number = room
    app.bed_number = bed
    app.status = "allocated"
    app.save()
    
    # Update occupied beds
    hostel.occupied_beds += 1
    hostel.save()
    
    return {"status": "allocated", "room": room, "bed": bed}


# --- EXAM SITINGS ---

@router.get("/exams", )
def list_exam_sittings(request, 
    course_id: Optional[str] = Query(None),
    semester_id: Optional[str] = Query(None),
    date: Optional[str] = Query(None)
):
    """List exam sittings"""
    from academic.models import ExamSitting
    queryset = ExamSitting.objects.all()
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    if semester_id:
        queryset = queryset.filter(semester_id=semester_id)
    if date:
        queryset = queryset.filter(date=date)
    return [
        {
            "id": str(e.id),
            "course": e.course.code if e.course else None,
            "semester": e.semester.name if e.semester else None,
            "venue": e.venue.name if e.venue else None,
            "date": str(e.date),
            "start_time": e.start_time,
            "end_time": e.end_time,
        }
        for e in queryset
    ]


@router.post("/exams")
def create_exam_sitting(request, data: ExamSittingSchema):
    """Schedule an exam"""
    from academic.models import ExamSitting, Course, Semester, Venue
    from students.models import User
    
    course = Course.objects.get(id=data.course_id)
    semester = Semester.objects.get(id=data.semester_id)
    venue = Venue.objects.get(id=data.venue_id)
    
    invigilator = None
    if data.invigilator_id:
        try:
            invigilator = User.objects.get(id=data.invigilator_id, user_type='staff')
        except:
            pass
    
    exam = ExamSitting.objects.create(
        course=course,
        semester=semester,
        venue=venue,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        invigilator=invigilator,
    )
    return exam


@router.get("/exams/course/{course_id}/semester/{semester_id}")
def get_course_exam(course_id: str, semester_id: str):
    """Get exam details for a course"""
    from academic.models import ExamSitting
    exam = ExamSitting.objects.filter(course_id=course_id, semester_id=semester_id).first()
    if not exam:
        return {"error": "Exam not scheduled"}
    return {
        "course": exam.course.code,
        "date": exam.date,
        "time": f"{exam.start_time}-{exam.end_time}",
        "venue": exam.venue.name,
        "invigilator": exam.invigilator.get_full_name() if exam.invigilator else "TBD",
    }


# ============= LIBRARY MANAGEMENT =============
LIBRARY_BOOKS = []
LIBRARY_LOANS = []


class BookSchema(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: str
    category: str
    total_copies: int = 1
    available_copies: int = 1


class LoanSchema(BaseModel):
    book_id: str
    student_id: str
    due_days: int = 14


@router.post("/library/books")
def add_book(request, data: BookSchema):
    """Add a book to library"""
    book = {
        "id": f"book-{len(LIBRARY_BOOKS)+1}",
        "isbn": data.isbn,
        "title": data.title,
        "author": data.author,
        "publisher": data.publisher,
        "category": data.category,
        "total_copies": data.total_copies,
        "available_copies": data.available_copies,
        "added_at": "2024-01-15"
    }
    LIBRARY_BOOKS.append(book)
    return {"success": True, "book": book}


@router.get("/library/books")
def search_books(request, query: Optional[str] = Query(None), category: Optional[str] = Query(None)):
    """Search library books"""
    results = LIBRARY_BOOKS
    if query:
        results = [b for b in results if query.lower() in b["title"].lower() or query.lower() in b["author"].lower()]
    if category:
        results = [b for b in results if b["category"] == category]
    return {"books": results}


@router.post("/library/borrow")
def borrow_book(request, data: LoanSchema):
    """Borrow a book"""
    book = next((b for b in LIBRARY_BOOKS if b["id"] == data.book_id), None)
    if not book or book["available_copies"] < 1:
        return {"success": False, "error": "Book not available"}
    
    from datetime import datetime, timedelta
    loan = {
        "id": f"loan-{len(LIBRARY_LOANS)+1}",
        "book_id": data.book_id,
        "student_id": data.student_id,
        "borrowed_at": "2024-01-15",
        "due_date": (datetime.now() + timedelta(days=data.due_days)).strftime("%Y-%m-%d"),
        "returned_at": None,
        "status": "active"
    }
    LIBRARY_LOANS.append(loan)
    
    book["available_copies"] -= 1
    return {"success": True, "loan": loan}


@router.post("/library/return/{loan_id}")
def return_book(request, loan_id: str):
    """Return a book"""
    loan = next((l for l in LIBRARY_LOANS if l["id"] == loan_id), None)
    if not loan:
        return {"error": "Loan not found"}
    
    loan["returned_at"] = "2024-01-20"
    loan["status"] = "returned"
    
    book = next((b for b in LIBRARY_BOOKS if b["id"] == loan["book_id"]), None)
    if book:
        book["available_copies"] += 1
    
    return {"success": True, "loan": loan}


@router.get("/library/loans/student/{student_id}")
def get_student_loans(request, student_id: str):
    """Get student's library loans"""
    loans = [l for l in LIBRARY_LOANS if l["student_id"] == student_id]
    return {"loans": loans}


# ============= ASSIGNMENT & QUIZ SYSTEM =============
ASSIGNMENTS = []


class AssignmentSchema(BaseModel):
    course_id: str
    title: str
    description: str
    due_date: str
    max_score: float = 100
    assignment_type: str = "homework"  # homework, quiz, project


@router.post("/assignments")
def create_assignment(request, data: AssignmentSchema):
    """Create an assignment"""
    assignment = {
        "id": f"assign-{len(ASSIGNMENTS)+1}",
        "course_id": data.course_id,
        "title": data.title,
        "description": data.description,
        "due_date": data.due_date,
        "max_score": data.max_score,
        "type": data.assignment_type,
        "created_at": "2024-01-15",
        "submissions": []
    }
    ASSIGNMENTS.append(assignment)
    return {"success": True, "assignment": assignment}


@router.get("/assignments/course/{course_id}")
def get_course_assignments(request, course_id: str):
    """Get assignments for a course"""
    assgns = [a for a in ASSIGNMENTS if a["course_id"] == course_id]
    return {"assignments": assgns}


class SubmissionSchema(BaseModel):
    assignment_id: str
    student_id: str
    content: str
    file_url: Optional[str] = None


@router.post("/assignments/{assignment_id}/submit")
def submit_assignment(request, assignment_id: str, data: SubmissionSchema):
    """Submit an assignment"""
    assignment = next((a for a in ASSIGNMENTS if a["id"] == assignment_id), None)
    if not assignment:
        return {"error": "Assignment not found"}
    
    submission = {
        "id": f"sub-{len(assignment['submissions'])+1}",
        "student_id": data.student_id,
        "content": data.content,
        "file_url": data.file_url,
        "submitted_at": "2024-01-15",
        "score": None,
        "feedback": None,
        "status": "submitted"
    }
    assignment["submissions"].append(submission)
    return {"success": True, "submission": submission}


# ============= LECTURER MANAGEMENT =============
LECTURERS = []


class LecturerSchema(BaseModel):
    staff_id: str
    first_name: str
    last_name: str
    email: str
    department_id: str
    qualification: str
    specialization: str


@router.post("/lecturers")
def add_lecturer(request, data: LecturerSchema):
    """Add a lecturer"""
    lecturer = {
        "id": f"lect-{len(LECTURERS)+1}",
        "staff_id": data.staff_id,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "email": data.email,
        "department_id": data.department_id,
        "qualification": data.qualification,
        "specialization": data.specialization,
        "courses": [],
        "created_at": "2024-01-15"
    }
    LECTURERS.append(lecturer)
    return {"success": True, "lecturer": lecturer}


@router.get("/lecturers")
def list_lecturers(request, department_id: Optional[str] = Query(None)):
    """List lecturers"""
    results = LECTURERS
    if department_id:
        results = [l for l in results if l["department_id"] == department_id]
    return {"lecturers": results}


@router.get("/lecturers/{lecturer_id}")
def get_lecturer(request, lecturer_id: str):
    """Get lecturer details"""
    lecturer = next((l for l in LECTURERS if l["id"] == lecturer_id), None)
    if not lecturer:
        return {"error": "Lecturer not found"}
    return lecturer


@router.post("/lecturers/{lecturer_id}/assign-course")
def assign_course(request, lecturer_id: str, course_id: str):
    """Assign course to lecturer"""
    lecturer = next((l for l in LECTURERS if l["id"] == lecturer_id), None)
    if not lecturer:
        return {"error": "Lecturer not found"}
    if course_id not in lecturer["courses"]:
        lecturer["courses"].append(course_id)
    return {"success": True, "lecturer": lecturer}


# ============= ALUMNI MODULE =============
ALUMNI = []


class AlumniSchema(BaseModel):
    student_id: str
    graduation_year: int
    degree: str
    current_employer: Optional[str] = None
    position: Optional[str] = None
    email: str
    phone: Optional[str] = None


@router.post("/alumni/register")
def register_alumni(request, data: AlumniSchema):
    """Register a graduate as alumni"""
    alumni = {
        "id": f"alum-{len(ALUMNI)+1}",
        "student_id": data.student_id,
        "graduation_year": data.graduation_year,
        "degree": data.degree,
        "current_employer": data.current_employer,
        "position": data.position,
        "email": data.email,
        "phone": data.phone,
        "registered_at": "2024-01-15",
        "status": "active"
    }
    ALUMNI.append(alumni)
    return {"success": True, "alumni": alumni}


@router.get("/alumni")
def list_alumni(request, graduation_year: Optional[int] = Query(None)):
    """List alumni"""
    results = ALUMNI
    if graduation_year:
        results = [a for a in results if a["graduation_year"] == graduation_year]
    return {"alumni": results}


@router.get("/alumni/{alumni_id}")
def get_alumni(request, alumni_id: str):
    """Get alumni details"""
    alumni = next((a for a in ALUMNI if a["id"] == alumni_id), None)
    if not alumni:
        return {"error": "Alumni not found"}
    return alumni


# ============= EXAM SEATING =============
SEATING_ARRANGEMENTS = []


@router.post("/exams/{exam_id}/seating/generate")
def generate_seating(request, exam_id: str):
    """Generate exam seating arrangement"""
    from random import shuffle
    
    # Demo: generate seating for 30 students
    students = [f"student-{i}" for i in range(1, 31)]
    shuffle(students)
    
    arrangement = {
        "exam_id": exam_id,
        "seats": [
            {"seat_number": i+1, "student_id": students[i], "row": (i // 6) + 1, "column": (i % 6) + 1}
            for i in range(len(students))
        ],
        "generated_at": "2024-01-15"
    }
    SEATING_ARRANGEMENTS.append(arrangement)
    return {"success": True, "arrangement": arrangement}


@router.get("/exams/{exam_id}/seating")
def get_seating(exam_id: str):
    """Get exam seating arrangement"""
    arr = next((a for a in SEATING_ARRANGEMENTS if a["exam_id"] == exam_id), None)
    if not arr:
        return {"error": "Seating not generated"}
    return arr


# ============= SIWES TRACKING (Polytechnic) =============
SIWES_REPORTS = []


class SiwesSchema(BaseModel):
    student_id: str
    company_name: str
    company_address: str
    supervisor_name: str
    supervisor_phone: str
    start_date: str
    end_date: str


@router.post("/siwes/register")
def register_siwes(request, data: SiwesSchema):
    """Register SIWES placement"""
    siwes = {
        "id": f"siwes-{len(SIWES_REPORTS)+1}",
        "student_id": data.student_id,
        "company_name": data.company_name,
        "company_address": data.company_address,
        "supervisor_name": data.supervisor_name,
        "supervisor_phone": data.supervisor_phone,
        "start_date": data.start_date,
        "end_date": data.end_date,
        "status": "active",
        "weekly_reports": [],
        "registered_at": "2024-01-15"
    }
    SIWES_REPORTS.append(siwes)
    return {"success": True, "siwes": siwes}


class SiwesWeeklyReport(BaseModel):
    siwes_id: str
    week: int
    activities: str
    supervisor_comment: Optional[str] = None


@router.post("/siwes/{siwes_id}/weekly-report")
def submit_weekly_report(request, siwes_id: str, data: SiwesWeeklyReport):
    """Submit weekly SIWES report"""
    siwes = next((s for s in SIWES_REPORTS if s["id"] == siwes_id), None)
    if not siwes:
        return {"error": "SIWES not found"}
    
    report = {
        "week": data.week,
        "activities": data.activities,
        "supervisor_comment": data.supervisor_comment,
        "submitted_at": "2024-01-15"
    }
    siwes["weekly_reports"].append(report)
    return {"success": True, "report": report}


@router.get("/siwes/student/{student_id}")
def get_student_siwes(request, student_id: str):
    """Get student's SIWES details"""
    siwes = next((s for s in SIWES_REPORTS if s["student_id"] == student_id), None)
    if not siwes:
        return {"error": "SIWES not found"}
    return siwes


# ============= COMPLAINT/TICKET SYSTEM =============
COMPLAINTS = []


class ComplaintSchema(BaseModel):
    student_id: str
    category: str  # academic, administrative, hostel, finance, other
    subject: str
    description: str
    priority: str = "normal"  # low, normal, high, urgent


@router.post("/complaints")
def submit_complaint(request, data: ComplaintSchema):
    """Submit a complaint/ticket"""
    complaint = {
        "id": f"complaint-{len(COMPLAINTS)+1}",
        "student_id": data.student_id,
        "category": data.category,
        "subject": data.subject,
        "description": data.description,
        "priority": data.priority,
        "status": "open",  # open, in_progress, resolved, closed
        "created_at": "2024-01-15",
        "responses": [],
        "assigned_to": None
    }
    COMPLAINTS.append(complaint)
    return {"success": True, "complaint": complaint}


@router.get("/complaints/student/{student_id}")
def get_student_complaints(request, student_id: str):
    """Get student's complaints"""
    comps = [c for c in COMPLAINTS if c["student_id"] == student_id]
    return {"complaints": comps}


@router.post("/complaints/{complaint_id}/respond")
def respond_complaint(request, complaint_id: str, response: str, assigned_to: Optional[str] = None):
    """Respond to a complaint"""
    complaint = next((c for c in COMPLAINTS if c["id"] == complaint_id), None)
    if not complaint:
        return {"error": "Complaint not found"}
    
    complaint["responses"].append({
        "response": response,
        "responded_at": "2024-01-15",
        "responded_by": assigned_to or "Admin"
    })
    
    if complaint["status"] == "open":
        complaint["status"] = "in_progress"
    
    return {"success": True, "complaint": complaint}


@router.post("/complaints/{complaint_id}/resolve")
def resolve_complaint(request, complaint_id: str, resolution: str):
    """Resolve a complaint"""
    complaint = next((c for c in COMPLAINTS if c["id"] == complaint_id), None)
    if not complaint:
        return {"error": "Complaint not found"}
    
    complaint["status"] = "resolved"
    complaint["resolution"] = resolution
    complaint["resolved_at"] = "2024-01-15"
    
    return {"success": True, "complaint": complaint}

# ============= AI/ML INTEGRATION =============



@router.get("/ai/prediction/student-success")
def predict_student_success(request, 
    student_id: str,
    gpa: float,
    attendance_rate: float,
    course_code: str,
    semester: str
):
    """Predict student success"""
    return {
        "student_id": student_id,
        "course_code": course_code,
        "predicted_score": round(75 + (gpa * 2.5) + (attendance_rate * 0.2), 1),
        "risk_level": "low" if gpa > 3.0 else "medium" if gpa > 2.0 else "high",
        "confidence": 0.82,
    }


@router.get("/ai/recommendations/{student_id}")
def get_recommendations(request, student_id: str):
    """Get personalized recommendations"""
    return {
        "student_id": student_id,
        "recommendations": [
            {"course": "CSC201", "type": "tutorial", "topic": "Data Structures"},
            {"course": "MTH201", "type": "practice", "topic": "Linear Algebra"},
        ],
    }

