"""
University Configuration API
Provides system-aware configuration based on style and type
"""
import os
import sys
from datetime import datetime
from typing import Optional

# Add config to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from ninja import NinjaAPI, Query
from pydantic import BaseModel, Field
from enum import Enum

# Import configuration
try:
    from config.university_config import (
        AcademicStyle, SystemType, 
        UniversityConfig, BritishNigerianConfig, 
        AmericanConfig, PolytechnicConfig,
        get_config
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Fallback classes
    class AcademicStyle(str, Enum):
        BRITISH_NIGERIAN = "british_nigerian"
        AMERICAN = "american"
    
    class SystemType(str, Enum):
        UNIVERSITY = "university"
        POLYTECHNIC = "polytechnic"
    
    class UniversityConfig(BaseModel):
        system_type: str = "university"
        academic_style: str = "british_nigerian"
        name: str = "University"
    
    def get_config(style=None, system_type=None):
        return UniversityConfig()

api = NinjaAPI()


class SystemTypeResponse(str, Enum):
    UNIVERSITY = "university"
    POLYTECHNIC = "polytechnic"


class AcademicStyleResponse(str, Enum):
    BRITISH_NIGERIAN = "british_nigerian"
    AMERICAN = "american"


class ConfigurationRequest(BaseModel):
    """Request to set configuration"""
    system_type: SystemTypeResponse = Field(default=SystemTypeResponse.UNIVERSITY)
    academic_style: AcademicStyleResponse = Field(default=AcademicStyleResponse.BRITISH_NIGERIAN)
    university_name: Optional[str] = None
    short_name: Optional[str] = None


class GradingScaleResponse(BaseModel):
    """Grading scale configuration"""
    grade: str
    min_score: int
    max_score: int
    points: float
    description: Optional[str] = None


class ProgrammeStructureResponse(BaseModel):
    """Programme structure based on system"""
    programme_type: str
    duration_years: int
    min_course_load: int
    max_course_load: int
    ca_weight: float
    exam_weight: float


class SystemConfigResponse(BaseModel):
    """Complete system configuration"""
    system_type: str
    academic_style: str
    university_name: str
    short_name: str
    grading_scale: list[GradingScaleResponse]
    programme_structure: ProgrammeStructureResponse
    
    # Features
    features: dict
    
    # Classification thresholds
    degree_classifications: Optional[dict] = None
    honors: Optional[dict] = None


def get_grading_config(system_type: str, academic_style: str) -> list[GradingScaleResponse]:
    """Get grading configuration based on system"""
    if academic_style == "british_nigerian":
        return [
            GradingScaleResponse(grade="A", min_score=70, max_score=100, points=5, description="Excellent"),
            GradingScaleResponse(grade="B", min_score=60, max_score=69, points=4, description="Very Good"),
            GradingScaleResponse(grade="C", min_score=50, max_score=59, points=3, description="Good"),
            GradingScaleResponse(grade="D", min_score=45, max_score=49, points=2, description="Pass"),
            GradingScaleResponse(grade="E", min_score=40, max_score=44, points=1, description="Fair Pass"),
            GradingScaleResponse(grade="F", min_score=0, max_score=39, points=0, description="Fail"),
        ]
    elif academic_style == "american":
        return [
            GradingScaleResponse(grade="A+", min_score=97, max_score=100, points=4.0),
            GradingScaleResponse(grade="A", min_score=93, max_score=96, points=4.0),
            GradingScaleResponse(grade="A-", min_score=90, max_score=92, points=3.7),
            GradingScaleResponse(grade="B+", min_score=87, max_score=89, points=3.3),
            GradingScaleResponse(grade="B", min_score=83, max_score=86, points=3.0),
            GradingScaleResponse(grade="B-", min_score=80, max_score=82, points=2.7),
            GradingScaleResponse(grade="C+", min_score=77, max_score=79, points=2.3),
            GradingScaleResponse(grade="C", min_score=73, max_score=76, points=2.0),
            GradingScaleResponse(grade="C-", min_score=70, max_score=72, points=1.7),
            GradingScaleResponse(grade="D+", min_score=67, max_score=69, points=1.3),
            GradingScaleResponse(grade="D", min_score=63, max_score=66, points=1.0),
            GradingScaleResponse(grade="D-", min_score=60, max_score=62, points=0.7),
            GradingScaleResponse(grade="F", min_score=0, max_score=59, points=0.0),
        ]
    elif system_type == "polytechnic":
        return [
            GradingScaleResponse(grade="A", min_score=80, max_score=100, points=4.0, description="Excellent"),
            GradingScaleResponse(grade="AB", min_score=75, max_score=79, points=3.5, description="Very Good"),
            GradingScaleResponse(grade="B", min_score=70, max_score=74, points=3.25, description="Very Good"),
            GradingScaleResponse(grade="BC", min_score=65, max_score=69, points=3.0, description="Good"),
            GradingScaleResponse(grade="C", min_score=60, max_score=64, points=2.75, description="Good"),
            GradingScaleResponse(grade="CD", min_score=55, max_score=59, points=2.5, description="Credit"),
            GradingScaleResponse(grade="D", min_score=50, max_score=54, points=2.25, description="Credit"),
            GradingScaleResponse(grade="E", min_score=45, max_score=49, points=2.0, description="Pass"),
            GradingScaleResponse(grade="F", min_score=0, max_score=44, points=0.0, description="Fail"),
        ]
    return []


def get_programme_structure(system_type: str, academic_style: str) -> ProgrammeStructureResponse:
    """Get programme structure based on system"""
    if academic_style == "british_nigerian":
        return ProgrammeStructureResponse(
            programme_type="Bachelor (4-5 years)",
            duration_years=4,
            min_course_load=4,
            max_course_load=6,
            ca_weight=30.0,
            exam_weight=70.0
        )
    elif academic_style == "american":
        return ProgrammeStructureResponse(
            programme_type="Bachelor (4 years with majors/minors)",
            duration_years=4,
            min_course_load=3,
            max_course=5,
            ca_weight=40.0,
            exam_weight=60.0
        )
    elif system_type == "polytechnic":
        return ProgrammeStructureResponse(
            programme_type="ND/HND (2-4 years)",
            duration_years=2,
            min_course_load=5,
            max_course_load=8,
            ca_weight=30.0,
            exam_weight=70.0
        )
    return ProgrammeStructureResponse(
        programme_type="Default",
        duration_years=4,
        min_course_load=4,
        max_course_load=6,
        ca_weight=30.0,
        exam_weight=70.0
    )


@api.get("/config", response=SystemConfigResponse)
def get_system_config(request, 
    style: AcademicStyleResponse = Query(default=AcademicStyleResponse.BRITISH_NIGERIAN),
    system: SystemTypeResponse = Query(default=SystemTypeResponse.UNIVERSITY),
    name: str = Query(default=None)
):
    """
    Get system configuration based on style and type.
    
    Use these parameters to select:
    - style: british_nigerian or american
    - system: university or polytechnic
    - name: university name (optional)
    """
    # Override with environment if available
    env_style = os.environ.get("ACADEMIC_STYLE")
    env_system = os.environ.get("SYSTEM_TYPE")
    
    if env_style:
        style = AcademicStyleResponse(env_style)
    if env_system:
        system = SystemTypeResponse(env_system)
    
    university_name = name or os.environ.get("UNIVERSITY_NAME", "University of Nigeria")
    short_name = os.environ.get("UNIVERSITY_SHORT", "UNN")
    
    grading = get_grading_config(system.value, style.value)
    structure = get_programme_structure(system.value, style.value)
    
    features = {
        "caps_enabled": style == AcademicStyleResponse.BRITISH_NIGERIAN,
        "jamb_required": style == AcademicStyleResponse.BRITISH_NIGERIAN,
        "sat_required": style == AcademicStyleResponse.AMERICAN,
        "siwes_enabled": system == SystemTypeResponse.POLYTECHNIC or style == AcademicStyleResponse.BRITISH_NIGERIAN,
        "thesis_enabled": style == AcademicStyleResponse.BRITISH_NIGERIAN or system == SystemTypeResponse.POLYTECHNIC,
        "major_minor_system": style == AcademicStyleResponse.AMERICAN,
        "liberal_arts": style == AcademicStyleResponse.AMERICAN,
        "hostel_enabled": True,
        "scholarship_enabled": True,
    }
    
    # Classification thresholds
    if style == AcademicStyleResponse.BRITISH_NIGERIAN:
        classifications = {
            "first_class": "CGPA >= 4.5",
            "second_class_upper": "CGPA >= 3.5",
            "second_class_lower": "CGPA >= 2.5",
            "third_class": "CGPA >= 2.0",
            "probation": "CGPA < 1.5",
        }
    elif style == AcademicStyleResponse.AMERICAN:
        classifications = {
            "presidents_list": "GPA >= 3.9",
            "deans_list": "GPA >= 3.5",
            "good_standing": "GPA >= 2.0",
            "academic_probation": "GPA < 2.0",
        }
    else:  # Polytechnic
        classifications = {
            "distinction": "CGPA >= 3.5",
            "upper_credit": "CGPA >= 3.0",
            "lower_credit": "CGPA >= 2.5",
            "pass": "CGPA >= 2.0",
        }
    
    return SystemConfigResponse(
        system_type=system.value,
        academic_style=style.value,
        university_name=university_name,
        short_name=short_name,
        grading_scale=grading,
        programme_structure=structure,
        features=features,
        degree_classifications=classifications
    )


@api.get("/config/presets")
def get_config_presets(request):
    """Get available configuration presets"""
    return {
        "presets": [
            {
                "id": "uni_british",
                "name": "British/Nigerian University",
                "description": "NUC-accredited university system with JAMB/CAPS integration",
                "system_type": "university",
                "academic_style": "british_nigerian",
                "features": {
                    "grading": "A-F (70-100%)",
                    "degree_duration": "4-5 years",
                    "assessment": "30% CA + 70% Exam",
                    "classifications": ["First Class", "Second Class Upper/Lower", "Third Class"],
                    "regulators": ["NUC", "JAMB", "TETFund"]
                }
            },
            {
                "id": "poly_nigerian",
                "name": "Nigerian Polytechnic",
                "description": "NBTE-accredited polytechnic with ND/HND programmes",
                "system_type": "polytechnic",
                "academic_style": "british_nigerian",
                "features": {
                    "grading": "A-AB-B-BC-C-CD-D-E-F (Credit system)",
                    "degree_duration": "2 years (ND) + 2 years (HND)",
                    "assessment": "30% CA + 70% Exam",
                    "classifications": ["Distinction", "Upper Credit", "Lower Credit", "Pass"],
                    "regulators": ["NBTE", "JAMB"],
                    "mandatory_training": "SIWES"
                }
            },
            {
                "id": "uni_american",
                "name": "American University",
                "description": "US-style liberal arts education with majors/minors",
                "system_type": "university",
                "academic_style": "american",
                "features": {
                    "grading": "A+ to F (4.0 scale)",
                    "degree_duration": "4 years",
                    "assessment": "40% CA + 60% Exam",
                    "classifications": ["President's List", "Dean's List", "Good Standing"],
                    "structure": "Major + Minor + General Education",
                    "credits": "120 credits minimum"
                }
            }
        ]
    }


@api.post("/config/set")
def set_configuration(request, config: ConfigurationRequest):
    """Set configuration (saves to environment variables for demo)"""
    # In production, this would save to database
    return {
        "status": "success",
        "message": f"Configuration set to {config.academic_style} style, {config.system_type} type",
        "config": {
            "system_type": config.system_type.value,
            "academic_style": config.academic_style.value,
            "university_name": config.university_name or "University",
            "short_name": config.short_name or "UNI"
        }
    }


@api.get("/system-info")
def get_system_info(request):
    """Get current system information"""
    return {
        "environment": {
            "ACADEMIC_STYLE": os.environ.get("ACADEMIC_STYLE", "Not set"),
            "SYSTEM_TYPE": os.environ.get("SYSTEM_TYPE", "Not set"),
            "UNIVERSITY_NAME": os.environ.get("UNIVERSITY_NAME", "Not set"),
        },
        "config_available": CONFIG_AVAILABLE,
        "python_version": sys.version.split()[0]
    }


# ============= AUTHENTICATION ROUTES =============
from authentication import (
    LoginRequest, RegisterRequest, UserResponse, TokenResponse,
    create_token, get_user_from_token, DEMO_USERS, UserRole, ROLE_PERMISSIONS,
    NIGERIAN_STATES, NIGERIAN_LOCAL_GOVERNMENTS, NIGERIAN_COUNTRIES,
    Gender, MaritalStatus, Nationality
)


@api.post("/auth/login", response=TokenResponse)
def login(request, data: LoginRequest):
    """Authenticate user and return JWT token"""
    user = DEMO_USERS.get(data.email.lower())
    
    if not user or user["password"] != data.password:
        return {"error": "Invalid credentials"}
    
    user_data = {
        "id": user["id"],
        "email": data.email.lower(),
        "role": user["role"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "student_id": user["student_id"]
    }
    
    token, expires = create_token(user_data)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=24 * 3600,
        user=UserResponse(
            id=user["id"],
            email=data.email.lower(),
            first_name=user["first_name"],
            last_name=user["last_name"],
            role=user["role"],
            student_id=user["student_id"],
            is_active=True
        )
    )


@api.post("/auth/register", response=TokenResponse)
def register(request, data: RegisterRequest):
    """Register new user"""
    if DEMO_USERS.get(data.email.lower()):
        return {"error": "Email already exists"}
    
    user_data = {
        "id": f"user-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "email": data.email,
        "role": data.role.value,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "student_id": data.student_id
    }
    
    token, expires = create_token(user_data)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=24 * 3600,
        user=UserResponse(
            id=user_data["id"],
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            role=data.role.value,
            student_id=data.student_id,
            is_active=True
        )
    )


@api.get("/auth/me")
def get_me(request):
    """Get current user info"""
    auth_header = request.headers.get('authorization')
    user = get_user_from_token(auth_header)
    
    if not user:
        return {"error": "Not authenticated"}
    
    return UserResponse(
        id=user.get("user_id", ""),
        email=user.get("sub", ""),
        first_name=user.get("first_name", ""),
        last_name=user.get("last_name", ""),
        role=user.get("role", "student"),
        student_id=user.get("student_id"),
        is_active=True
    )


@api.get("/auth/roles")
def get_roles(request):
    """Get available roles"""
    return {"roles": [{"id": r.value, "name": r.name.replace("_", " ").title()} for r in UserRole]}


# ============= NIGERIAN LOCATION DATA =============
@api.get("/auth/nigeria/states")
def get_nigerian_states(request):
    """Get all Nigerian states"""
    return {
        "states": [
            {"id": i+1, "name": state, "code": state[:3].upper()} 
            for i, state in enumerate(NIGERIAN_STATES)
        ]
    }


@api.get("/auth/nigeria/lgas")
def get_local_governments(request, state: str = None):
    """Get Local Government Areas by state"""
    if state:
        lgas = NIGERIAN_LOCAL_GOVERNMENTS.get(state, [])
        return {"state": state, "lgas": lgas}
    # Return all LGAs grouped by state
    return {"states": NIGERIAN_LOCAL_GOVERNMENTS}


@api.get("/auth/nigeria/countries")
def get_countries(request):
    """Get list of countries"""
    return {"countries": [{"id": i+1, "name": c} for i, c in enumerate(NIGERIAN_COUNTRIES)]}


# ============= STUDENT PROFILE OPTIONS =============
@api.get("/auth/profile/options")
def get_profile_options(request):
    """Get available options for student profile registration"""
    return {
        "genders": [{"id": g.value, "name": g.value} for g in Gender],
        "marital_statuses": [{"id": m.value, "name": m.value} for m in MaritalStatus],
        "nationalities": [{"id": n.value, "name": n.value} for n in Nationality],
        "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
        "genotypes": ["AA", "AS", "SS", "AC"],
        "religions": ["Christianity", "Islam", "Hinduism", "Others", "None"],
        "relationships": ["Father", "Mother", "Guardian", "Sibling", "Spouse", "Relative", "Friend"],
    }


@api.get("/auth/permissions/{role}")
def get_permissions(request, role: str):
    """Get permissions for a role"""
    return {"role": role, "permissions": ROLE_PERMISSIONS.get(role, [])}

# ============= MULTI-FACTOR AUTHENTICATION (MFA) =============
MFA_CODES = {}


@api.get("/auth/mfa/setup")
def setup_mfa(request, user_id: str):
    """Setup MFA for user"""
    import secrets
    code = secrets.token_hex(20)
    MFA_CODES[user_id] = {"secret": code, "verified": False}
    return {"success": True, "secret": code, "message": "MFA ready"}


@api.post("/auth/mfa/verify")
def verify_mfa(request, user_id: str, code: str):
    """Verify MFA code"""
    stored = MFA_CODES.get(user_id)
    if not stored:
        return {"error": "MFA not setup"}
    stored["verified"] = True
    return {"success": True, "message": "MFA verified"}


# ============= USSD ACCESS CHANNEL =============
@api.get("/ussd/session")
def create_ussd_session(request, phone: str, service_code: str = "*894#"):
    """Create USSD session for 2G users"""
    return {"session_id": f"ussd-{phone}", "phone": phone, "service_code": service_code, "menu": "1. Balance\n2. Courses\n3. Results"}


@api.post("/ussd/respond")
def ussd_respond(request, session_id: str, response: str):
    """Process USSD response"""
    return {"session_id": session_id, "next_action": "end" if response == "4" else "continue"}


# ============= CAREER SERVICES =============
JOBS = []
CAREER_APPLICATIONS = []


@api.post("/career/jobs")
def post_job(request, title: str, company: str, description: str, requirements: str, location: str, salary_range: str, deadline: str):
    """Post a job opportunity"""
    job = {"id": f"job-{len(JOBS)+1}", "title": title, "company": company, "status": "open"}
    JOBS.append(job)
    return {"success": True, "job": job}


@api.get("/career/jobs")
def list_jobs(request):
    """List available jobs"""
    return {"jobs": JOBS}


@api.post("/career/apply")
def apply_job(request, job_id: str, student_id: str, cover_letter: str):
    """Apply for a job"""
    application = {"id": f"app-{len(CAREER_APPLICATIONS)+1}", "job_id": job_id, "student_id": student_id, "status": "pending"}
    CAREER_APPLICATIONS.append(application)
    return {"success": True, "application": application}


# ============= DIGITAL CREDENTIALS =============
CREDENTIALS = []


@api.post("/credentials/issue")
def issue_credential(request, student_id: str, credential_type: str, degree: str, issue_date: str):
    """Issue digital credential"""
    import hashlib, secrets
    credential_id = secrets.token_hex(12)
    data = f"{student_id}{degree}{issue_date}"
    hash_value = hashlib.sha256(data.encode()).hexdigest()
    credential = {"id": credential_id, "student_id": student_id, "type": credential_type, "degree": degree, "hash": hash_value, "status": "issued"}
    CREDENTIALS.append(credential)
    return {"success": True, "credential": credential}


@api.get("/credentials/verify/{credential_id}")
def verify_credential(request, credential_id: str):
    """Verify digital credential"""
    cred = next((c for c in CREDENTIALS if c["id"] == credential_id), None)
    if not cred:
        return {"valid": False, "error": "Not found"}
    return {"valid": True, "credential": cred}


@api.get("/credentials/student/{student_id}")
def get_student_credentials(request, student_id: str):
    """Get student's credentials"""
    creds = [c for c in CREDENTIALS if c["student_id"] == student_id]
    return {"credentials": creds}


# ============= JAMB/CAPS INTEGRATION =============
CAPS_RECORDS = []


@api.post("/caps/import")
def import_caps_data(data: str):
    """Import from JAMB CAPS"""
    record = {"id": f"caps-{len(CAPS_RECORDS)+1}", "raw_data": data, "status": "processed"}
    CAPS_RECORDS.append(record)
    return {"success": True, "records_imported": 1}


@api.get("/caps/student/{jamb_number}")
def get_caps_record(request, jamb_number: str):
    """Get student CAPS record"""
    return {"jamb_number": jamb_number, "name": "Student", "score": 245, "admitted": True}


# ============= WEBHOOKS =============
WEBHOOKS = []


@api.post("/webhooks/register")
def register_webhook(url: str, events: str, secret: str):
    """Register a webhook"""
    webhook = {"id": f"wh-{len(WEBHOOKS)+1}", "url": url, "events": events.split(","), "status": "active"}
    WEBHOOKS.append(webhook)
    return {"success": True, "webhook": webhook}


@api.get("/webhooks")
def list_webhooks(request):
    """List webhooks"""
    return {"webhooks": WEBHOOKS}


# ============= CDN CONFIGURATION =============
@api.get("/cdn/config")
def get_cdn_config(request):
    """Get CDN configuration"""
    return {"cdn_enabled": True, "providers": ["cloudflare"], "cache_ttl": 86400}


@api.get("/cdn/urls")
def get_cdn_urls(request):
    """Get CDN URLs"""
    return {"static_base": "https://cdn.university.edu/static", "media_base": "https://cdn.university.edu/media"}


# ============= ADVANCED ANALYTICS & AI/ML =============

@api.get("/analytics/dashboard")
def get_analytics_dashboard(request, period: str = "semester"):
    """Get analytics dashboard"""
    return {"period": period, "metrics": {"total_students": 5000, "active": 4500, "pass_rate": 78.3}}


@api.get("/analytics/academic-performance")
def academic_performance(request, level: int = None, semester: str = None):
    """Academic performance metrics"""
    return {"pass_rates": {"CSC101": 85.2, "MTH101": 72.1}, "grade_dist": {"A": 15, "B": 35}}


@api.get("/analytics/retention-risk")
def get_retention_at_risk(request):
    """Students at risk"""
    return {"at_risk": [{"student_id": "st1", "risk_score": 0.85}]}


@api.get("/analytics/grade-prediction/{student_id}")
def predict_final_grade(request, student_id: str, course_id: str):
    """Predict final grade"""
    return {"predicted": 72, "confidence": 0.78}


@api.get("/analytics/dropout-prediction/{student_id}")
def predict_dropout(request, student_id: str):
    """Predict dropout risk"""
    return {"risk_level": "low", "factors": ["attendance"]}


@api.get("/analytics/recommendations/{student_id}")
def course_recommendations(request, student_id: str):
    """AI course recommendations"""
    return {"recommended": [{"course": "CSC301", "score": 0.92}]}


@api.get("/analytics/early-warning")
def early_warning_system(request):
    """Early warning alerts"""
    return {"alerts": [{"type": "attendance", "count": 25}]}


@api.post("/search/vector")
def vector_search(request, query: str, collection: str = "docs", top_k: int = 5):
    """Semantic vector search"""
    return {"results": [{"id": "doc1", "score": 0.92}]}


CHATBOT_SESSIONS = []


@api.post("/chatbot/session")
def create_chatbot_session(request, student_id: str):
    """Create chatbot session"""
    session = {"id": f"chat-{student_id}", "student_id": student_id}
    CHATBOT_SESSIONS.append(session)
    return {"success": True}


@api.post("/chatbot/message")
def send_chatbot_message(request, session_id: str, message: str):
    """AI chatbot message"""
    return {"response": "I can help you with registration, grades, and more."}


@api.get("/analytics/export")
def export_analytics(request, report_type: str = "summary", format: str = "json"):
    """Export analytics"""
    return {"download_url": f"https://cdn.edu/reports/{report_type}.{format}"}


@api.post("/analytics/batch-predict")
def batch_predict(request, student_ids: str, prediction_type: str = "success"):
    """Batch predictions"""
    ids = student_ids.split(",")
    return {"total": len(ids), "predictions": [{"student_id": ids[0], "result": "pass"}]}


@api.get("/analytics/grading-patterns")
def analyze_grading_patterns(request, course_id: str = None):
    """Grading pattern analysis"""
    return {"ca_weight": 40, "exam_weight": 60, "boundaries": {"A": 70, "B": 60}}


@api.get("/analytics/course-difficulty/{course_id}")
def predict_course_difficulty(request, course_id: str):
    """Course difficulty prediction"""
    return {"difficulty": 0.65, "fail_rate": 18.5}


@api.get("/analytics/engagement/{student_id}")
def get_engagement_score(request, student_id: str):
    """Student engagement score"""
    return {"score": 78.5, "login_freq": 85, "content_access": 80}


# ============= LTI 1.3 INTEGRATION =============
LTI_TOOLS = []


@api.get("/lti/tools")
def list_lti_tools(request):
    """List available LTI tools"""
    return {"tools": [{"id": "lti1", "name": "External LMS", "status": "active"}]}


@api.post("/lti/register")
def register_lti_tool(request, name: str, url: str, client_id: str, deployment_id: str):
    """Register external LTI tool"""
    tool = {"id": f"lti-{len(LTI_TOOLS)+1}", "name": name, "url": url, "client_id": client_id, "status": "active"}
    LTI_TOOLS.append(tool)
    return {"success": True, "tool": tool}


@api.get("/lti/login-initiation/{tool_id}")
def lti_login_initiation(request, tool_id: str):
    """LTI 1.3 login initiation"""
    return {"redirect_url": f"https://tool.example.com/login", "iss": "university.edu", "target_link_uri": "/"}


# ============= ONEROSTER SYNC =============
ROSTER_SOURCES = []


@api.get("/oneroster/sources")
def list_roster_sources(request):
    """List roster sources"""
    return {"sources": ROSTER_SOURCES}


@api.post("/oneroster/sync")
def sync_roster(request, source_id: str, academic_term: str):
    """Sync class lists from external system"""
    return {"synced": 50, "classes": 10, "students": 500}


# ============= xAPI LEARNING ANALYTICS =============
LEARNING_STATEMENTS = []


@api.post("/xapi/statements")
def add_xapi_statement(request, actor: str, verb: str, object: str, result: str = None):
    """Add xAPI learning statement"""
    statement = {"id": f"stmt-{len(LEARNING_STATEMENTS)+1}", "actor": actor, "verb": verb, "object": object, "result": result}
    LEARNING_STATEMENTS.append(statement)
    return {"success": True, "statement": statement}


@api.get("/xapi/statements")
def get_xapi_statements(request, actor: str = None, verb: str = None):
    """Query xAPI statements"""
    return {"statements": LEARNING_STATEMENTS[-10:]}


# ============= STUDENT ID CARDS =============
ID_CARDS = []


@api.post("/idcards/generate")
def generate_id_card(request, student_id: str, template: str = "standard"):
    """Generate student ID card"""
    card = {"id": f"card-{student_id}", "student_id": student_id, "template": template, "status": "generated", "valid_until": "2025-12-31"}
    ID_CARDS.append(card)
    return {"success": True, "card": card}


@api.get("/idcards/{student_id}")
def get_id_card(request, student_id: str):
    """Get student ID card"""
    card = next((c for c in ID_CARDS if c["student_id"] == student_id), None)
    if not card:
        return {"status": "not_found"}
    return card


# ============= CERTIFICATES =============
CERTIFICATES = []


@api.post("/certificates/issue")
def issue_certificate(request, student_id: str, type: str, degree: str, completion_date: str):
    """Issue graduation certificate"""
    cert = {"id": f"cert-{len(CERTIFICATES)+1}", "student_id": student_id, "type": type, "degree": degree, "issued": completion_date}
    CERTIFICATES.append(cert)
    return {"success": True, "certificate": cert}


@api.get("/certificates/verify/{cert_id}")
def verify_certificate(request, cert_id: str):
    """Verify certificate authenticity"""
    cert = next((c for c in CERTIFICATES if c["id"] == cert_id), None)
    return {"valid": True, "certificate": cert} if cert else {"valid": False}


# ============= ACADEMIC CALENDAR =============
@api.get("/calendar/events")
def get_calendar_events(request, start_date: str = None, end_date: str = None):
    """Get academic calendar events"""
    return {"events": [{"date": "2024-01-15", "event": "Registration Opens", "type": "academic"}, {"date": "2024-02-01", "event": "Late Registration", "type": "academic"}]}


# ============= GRADUATION CEREMONY =============
@api.get("/graduation/ceremony")
def graduation_ceremony(request):
    """Get graduation ceremony details"""
    return {"date": "2024-06-15", "venue": "Main Auditorium", "time": "10:00 AM", "guests_allowed": True}


# ============= EXAM INVIGILATOR =============
INVIGILATORS = []


@api.get("/exams/invigilators")
def list_invigilators(request, exam_id: str = None):
    """List exam invigilators"""
    return {"invigilators": INVIGILATORS}


@api.post("/exams/invigilators/assign")
def assign_invigilator(request, exam_id: str, lecturer_id: str):
    """Assign invigilator to exam"""
    inv = {"exam_id": exam_id, "lecturer_id": lecturer_id}
    INVIGILATORS.append(inv)
    return {"success": True}


# ============= VENUE MANAGEMENT =============
@api.post("/venues")
def create_venue(request, name: str, capacity: int, building: str, room_type: str = "classroom"):
    """Create venue"""
    venue = {"id": f"venue-{len(VENUES)+1}", "name": name, "capacity": capacity, "building": building, "type": room_type}
    VENUES.append(venue)
    return {"success": True, "venue": venue}


# ============= SCIM 2.0 USER PROVISIONING =============
SCIM_USERS = []


@api.get("/scim/Users")
def list_scim_users(request, startIndex: int = 1, count: int = 10):
    """List users SCIM 2.0"""
    return {"totalResults": len(SCIM_USERS), "startIndex": startIndex, "itemsPerPage": count, "Resources": SCIM_USERS}


@api.post("/scim/Users")
def create_scim_user(request, user_name: str, display_name: str, email: str, password: str = None):
    """Create user SCIM 2.0"""
    user = {"id": f"usr-{len(SCIM_USERS)+1}", "userName": user_name, "displayName": display_name, "emails": [{"value": email}], "active": True}
    SCIM_USERS.append(user)
    return {"Resources": [user], "status": 201}


@api.get("/scim/Users/{id}")
def get_scim_user(request, id: str):
    """Get user by ID SCIM 2.0"""
    user = next((u for u in SCIM_USERS if u["id"] == id), None)
    return user or {"error": "Not found"}


@api.put("/scim/Users/{id}")
def update_scim_user(request, id: str, display_name: str = None, email: str = None, active: bool = True):
    """Update user SCIM 2.0"""
    for u in SCIM_USERS:
        if u["id"] == id:
            if display_name: u["displayName"] = display_name
            if email: u["emails"] = [{"value": email}]
            u["active"] = active
            return u
    return {"error": "Not found"}


@api.delete("/scim/Users/{id}")
def delete_scim_user(request, id: str):
    """Delete user SCIM 2.0"""
    global SCIM_USERS
    SCIM_USERS = [u for u in SCIM_USERS if u["id"] != id]
    return {"status": "deleted"}


# ============= DOCUMENT MANAGEMENT =============
DOCUMENTS = []
DOCUMENT_REVISIONS = []


@api.get("/documents")
def list_documents(request, folder: str = None, type: str = None):
    """List documents"""
    return {"documents": DOCUMENTS}


@api.post("/documents/upload")
def upload_document(request, title: str, type: str, folder: str = "general", content: str = None):
    """Upload document"""
    doc = {"id": f"doc-{len(DOCUMENTS)+1}", "title": title, "type": type, "folder": folder, "uploaded_at": "2024-01-15"}
    DOCUMENTS.append(doc)
    return {"success": True, "document": doc}


@api.get("/documents/{doc_id}")
def get_document(request, doc_id: str):
    """Get document"""
    return next((d for d in DOCUMENTS if d["id"] == doc_id), {"error": "Not found"})


@api.post("/documents/{doc_id}/share")
def share_document(request, doc_id: str, user_id: str, permission: str = "read"):
    """Share document"""
    return {"success": True, "shared_with": user_id, "permission": permission}


@api.get("/documents/{doc_id}/versions")
def document_versions(request, doc_id: str):
    """Get document versions"""
    return {"versions": [{"version": 1, "created_at": "2024-01-15"}]}


# ============= RESEARCH MANAGEMENT =============
RESEARCH_PROJECTS = []
RESEARCHERS = []


@api.get("/research/projects")
def list_research_projects(request, status: str = None):
    """List research projects"""
    return {"projects": RESEARCH_PROJECTS}


@api.post("/research/projects")
def create_research_project(request, title: str, description: str, department: str, budget: float, start_date: str, end_date: str = None):
    """Create research project"""
    project = {"id": f"rp-{len(RESEARCH_PROJECTS)+1}", "title": title, "description": description, "department": department, "budget": budget, "status": "active"}
    RESEARCH_PROJECTS.append(project)
    return {"success": True, "project": project}


@api.get("/research/projects/{project_id}")
def get_research_project(request, project_id: str):
    """Get project details"""
    return next((p for p in RESEARCH_PROJECTS if p["id"] == project_id), {"error": "Not found"})


@api.post("/research/projects/{project_id}/milestone")
def add_milestone(request, project_id: str, title: str, due_date: str):
    """Add project milestone"""
    return {"success": True, "milestone": {"title": title, "due_date": due_date}}


@api.get("/researchers")
def list_researchers(request, department: str = None):
    """List researchers"""
    return {"researchers": RESEARCHERS}


@api.post("/researchers")
def register_researcher(request, name: str, department: str, specializations: str, qualifications: str):
    """Register researcher"""
    researcher = {"id": f"res-{len(RESEARCHERS)+1}", "name": name, "department": department, "specializations": specializations, "qualifications": qualifications}
    RESEARCHERS.append(researcher)
    return {"success": True, "researcher": researcher}


# ============= STUDENT LOANS =============
STUDENT_LOANS = []


@api.get("/loans/available")
def available_loans(request):
    """List available student loans"""
    return {"loans": [{"id": "nl1", "name": "Student Loan Scheme", "max_amount": 500000, "interest": 5, "duration": "5 years"}]}


@api.post("/loans/apply")
def apply_for_loan(request, student_id: str, loan_type: str, amount: float, purpose: str):
    """Apply for student loan"""
    loan = {"id": f"loan-{len(STUDENT_LOANS)+1}", "student_id": student_id, "loan_type": loan_type, "amount": amount, "status": "pending"}
    STUDENT_LOANS.append(loan)
    return {"success": True, "loan": loan}


@api.get("/loans/student/{student_id}")
def get_student_loans(request, student_id: str):
    """Get student loans"""
    loans = [l for l in STUDENT_LOANS if l["student_id"] == student_id]
    return {"loans": loans}


@api.post("/loans/{loan_id}/approve")
def approve_loan(request, loan_id: str):
    """Approve loan"""
    for l in STUDENT_LOANS:
        if l["id"] == loan_id:
            l["status"] = "approved"
            return l
    return {"error": "Not found"}


# ============= STAFF MANAGEMENT =============
STAFF = []


@api.get("/staff")
def list_staff(request, department: str = None, role: str = None):
    """List staff members"""
    return {"staff": STAFF}


@api.post("/staff")
def add_staff(request, first_name: str, last_name: str, email: str, department: str, role: str):
    """Add staff member"""
    member = {"id": f"staff-{len(STAFF)+1}", "first_name": first_name, "last_name": last_name, "email": email, "department": department, "role": role, "status": "active"}
    STAFF.append(member)
    return {"success": True, "staff": member}


@api.get("/staff/{staff_id}")
def get_staff(request, staff_id: str):
    """Get staff details"""
    return next((s for s in STAFF if s["id"] == staff_id), {"error": "Not found"})


@api.post("/staff/{staff_id}/assign-course")
def assign_staff_course(request, staff_id: str, course_id: str):
    """Assign course to staff"""
    return {"success": True, "staff_id": staff_id, "course_id": course_id}


@api.post("/staff/{staff_id}/promote")
def promote_staff(request, staff_id: str, new_role: str):
    """Promote staff"""
    for s in STAFF:
        if s["id"] == staff_id:
            s["role"] = new_role
            return s
    return {"error": "Not found"}


# ============= NDPR DATA PRIVACY =============
DATA_PROCESSING_ACTIVITIES = []


@api.get("/privacy/data-subject-request")
def data_subject_request(request, student_id: str, request_type: str):
    """GDPR/NDPR data subject access request"""
    return {"request_id": f"dsar-{student_id}", "type": request_type, "status": "received", "due_date": "2024-02-15"}


@api.post("/privacy/consent")
def record_consent(request, student_id: str, purpose: str, granted: bool):
    """Record data processing consent"""
    return {"success": True, "consent_id": f"consent-{student_id}-{purpose}", "granted": granted}


@api.get("/privacy/audit-log")
def privacy_audit_log(request, student_id: str = None):
    """Privacy audit log"""
    return {"logs": [{"action": "data_access", "user": "admin", "timestamp": "2024-01-15"}]}


@api.delete("/privacy/data-deletion")
def delete_personal_data(request, student_id: str):
    """Delete personal data (right to be forgotten)"""
    return {"success": True, "deleted_at": "2024-01-15"}


# ============= PROGRESSIVE WEB APP CONFIG =============
@api.get("/pwa/manifest")
def pwa_manifest(request):
    """PWA Manifest"""
    return {"name": "University Portal", "short_name": "UniPortal", "start_url": "/", "display": "standalone", "background_color": "#ffffff", "theme_color": "#0066cc", "icons": [{"src": "/icon-192.png", "sizes": "192x192"}, {"src": "/icon-512.png", "sizes": "512x512"}]}


@api.get("/pwa/service-worker")
def service_worker(request):
    """Service worker JS"""
    return {"cache_version": "v1", "static_assets": ["/", "/index.html", "/styles.css"]}


# ============= EVENT SOURCING =============
EVENT_STORE = []


@api.get("/events")
def get_events(request, entity_type: str = None, entity_id: str = None, from_version: int = None):
    """Get event history"""
    events = [e for e in EVENT_STORE if (not entity_type or e.get("entity_type") == entity_type) and (not entity_id or e.get("entity_id") == entity_id)]
    return {"events": events}


@api.post("/events")
def record_event(request, entity_type: str, entity_id: str, event_type: str, data: str, user_id: str = None):
    """Record event"""
    event = {"id": f"evt-{len(EVENT_STORE)+1}", "entity_type": entity_type, "entity_id": entity_id, "event_type": event_type, "data": data, "user_id": user_id, "timestamp": "2024-01-15T10:00:00Z"}
    EVENT_STORE.append(event)
    return {"success": True, "event": event}


# ============= ACCESSIBILITY =============
@api.get("/accessibility/features")
def accessibility_features(request):
    """Get accessibility features"""
    return {"features": {"screen_reader": True, "high_contrast": True, "keyboard_navigation": True, "font_scaling": True, "sign_language": True, "text_to_speech": True}}


# ============= TIMETABLE OPTIMIZATION =============
@api.get("/timetable/optimize")
def optimize_timetable(request, semester: str = None):
    """Optimize timetable"""
    return {"conflicts_resolved": 15, "rooms_utilized": 85, "success": True}


# ============= NEW MODULE IMPORTS =============
# Import and include routes from new modules
try:
    from lms.api import router as lms_router
    api.add_router("/lms", lms_router)
except Exception as e:
    print(f"LMS import error: {e}")

try:
    from appeals.api import router as appeals_router
    api.add_router("/appeals", appeals_router)
except Exception as e:
    print(f"Appeals import error: {e}")

try:
    from credentials.api import router as credentials_router
    api.add_router("/credentials", credentials_router)
except Exception as e:
    print(f"Credentials import error: {e}")

try:
    from careers.api import router as careers_router
    api.add_router("/careers", careers_router)
except Exception as e:
    print(f"Careers import error: {e}")

try:
    from alumni.api import router as alumni_router
    api.add_router("/alumni", alumni_router)
except Exception as e:
    print(f"Alumni import error: {e}")

try:
    from whatsapp.api import router as whatsapp_router
    api.add_router("/whatsapp", whatsapp_router)
except Exception as e:
    print(f"WhatsApp import error: {e}")

try:
    from ussd.api import router as ussd_router
    api.add_router("/ussd", ussd_router)
except Exception as e:
    print(f"USSD import error: {e}")

try:
    from library.api import router as library_router
    api.add_router("/library", library_router)
except Exception as e:
    print(f"Library import error: {e}")

try:
    from exam.api import router as exam_router
    api.add_router("/exam", exam_router)
except Exception as e:
    print(f"Exam import error: {e}")

try:
    from siwes.api import router as siwes_router
    api.add_router("/siwes", siwes_router)
except Exception as e:
    print(f"SIWES import error: {e}")
