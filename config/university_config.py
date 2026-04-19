# University Portal Configuration System
# Supports British/Nigerian and American university systems

import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from functools import lru_cache


class SystemType(str, Enum):
    """Academic system types"""
    UNIVERSITY = "university"
    POLYTECHNIC = "polytechnic"


class AcademicStyle(str, Enum):
    """Academic style/framework"""
    BRITISH_NIGERIAN = "british_nigerian"  # NUC, JAMB, TETFund aligned
    AMERICAN = "american"  # US-style liberal arts + majors


class UniversityConfig(BaseModel):
    """Main university configuration"""
    
    # System Identification
    system_type: SystemType = SystemType.UNIVERSITY
    academic_style: AcademicStyle = AcademicStyle.BRITISH_NIGERIAN
    
    # University Details
    name: str = "University of Nigeria"
    short_name: str = "UNN"
    code: str = "UNN"  # JAMB institution code
    
    # Regulatory Alignment
    nuc_accredited: bool = True
    tetfund_qualified: bool = True
    
    # Academic Structure
    max_course_load: int = 6  # Maximum courses per semester
    min_course_load: int = 4  # Minimum courses per semester
    
    # Grading System (will be different based on style)
    grading_scale: str = "default"
    
    # Academic Calendar
    sessions_per_year: int = 2  # Two semesters typically
    
    # Features
    hostel_enabled: bool = True
    siwes_enabled: bool = True  # Industrial Training
    project_enabled: bool = True
    thesis_enabled: bool = True
    
    # AI Features
    predictive_analytics_enabled: bool = True
    chatbot_enabled: bool = True
    
    class Config:
        arbitrary_types_allowed = True


class BritishNigerianConfig(UniversityConfig):
    """Configuration for British/Nigerian university system"""
    
    academic_style: AcademicStyle = AcademicStyle.BRITISH_NIGERIAN
    
    # Nigerian-specific settings
    caps_enabled: bool = True  # JAMB CAPS integration
    jamb_required: bool = True  # JAMB UTME required
    
    # Degree structure
    programmes_levels: int = 4  # 4-year undergraduate (most)
    professional_years: int = 5  # Medicine, Law, Engineering
    
    # Assessment
    continuous_assessment_weight: float = 30.0  # CA out of 100
    exam_weight: float = 70.0
    
    # Grading (Nigerian scale)
    grading_config = {
        "A": {"min": 70, "max": 100, "points": 5, "description": "Excellent"},
        "B": {"min": 60, "max": 69, "points": 4, "description": "Very Good"},
        "C": {"min": 50, "max": 59, "points": 3, "description": "Good"},
        "D": {"min": 45, "max": 49, "points": 2, "description": "Pass"},
        "E": {"min": 40, "max": 44, "points": 1, "description": "Fair Pass"},
        "F": {"min": 0, "max": 39, "points": 0, "description": "Fail"},
    }
    
    # Degree classifications
    first_class: float = 4.5  # CGPA >= 4.5
    second_class_upper: float = 3.5  # CGPA >= 3.5
    second_class_lower: float = 2.5  # CGPA >= 2.5
    third_class: float = 2.0  # CGPA >= 2.0
    
    # Academic probation
    probation_gpa: float = 1.5  # Below this = probation
    suspension_gpa: float = 1.0  # Below this = suspension
    
    # Professional courses (e.g., Medicine)
    professional_programmes = [
        "Medicine", "Law", "Engineering", "Pharmacy", "Dentistry"
    ]


class AmericanConfig(UniversityConfig):
    """Configuration for American university system"""
    
    academic_style: AcademicStyle = AcademicStyle.AMERICAN
    
    # US-style settings
    sat_required: bool = True  # SAT/ACT for admissions
    gpa_scale: float = 4.0  # 4.0 scale
    
    # Degree structure
    typical_years: int = 4  # 4-year bachelor's
    liberal_arts: bool = True  # Liberal arts foundation
    
    # Major/Minor system
    major_required: bool = True
    minor_optional: bool = True
    general_education_credits: int = 40  # Gen ed requirements
    
    # Grading (US scale)
    grading_config = {
        "A+": {"min": 97, "max": 100, "points": 4.0},
        "A": {"min": 93, "max": 96, "points": 4.0},
        "A-": {"min": 90, "max": 92, "points": 3.7},
        "B+": {"min": 87, "max": 89, "points": 3.3},
        "B": {"min": 83, "max": 86, "points": 3.0},
        "B-": {"min": 80, "max": 82, "points": 2.7},
        "C+": {"min": 77, "max": 79, "points": 2.3},
        "C": {"min": 73, "max": 76, "points": 2.0},
        "C-": {"min": 70, "max": 72, "points": 1.7},
        "D+": {"min": 67, "max": 69, "points": 1.3},
        "D": {"min": 63, "max": 66, "points": 1.0},
        "D-": {"min": 60, "max": 62, "points": 0.7},
        "F": {"min": 0, "max": 59, "points": 0.0},
    }
    
    # Dean's list
    deans_list_gpa: float = 3.5
    presidents_list_gpa: float = 3.9
    
    # Credit system
    credits_per_course: int = 3  # Typical credit hours
    min_credits_for_degree: int = 120
    credits_per_semester: int = 15


class PolytechnicConfig(UniversityConfig):
    """Configuration for Nigerian polytechnic system"""
    
    system_type: SystemType = SystemType.POLYTECHNIC
    
    # Polytechnic-specific
    nbte_accredited: bool = True  # National Board for Technical Education
    hands_on_training: bool = True
    mandatory_siwes: bool = True  # Industrial Attachment
    
    # HND vs ND
    higher_national_diploma: bool = True  # HND after ND
    
    # Programmes
    nbc_levels = ["ND", "HND"]  # National Diploma, Higher National Diploma
    
    # Grading (Polytechnic scale)
    grading_config = {
        "A": {"min": 80, "max": 100, "points": 4.0, "description": "Excellent"},
        "AB": {"min": 75, "max": 79, "points": 3.5, "description": "Very Good"},
        "B": {"min": 70, "max": 74, "points": 3.25, "description": "Very Good"},
        "BC": {"min": 65, "max": 69, "points": 3.0, "description": "Good"},
        "C": {"min": 60, "max": 64, "points": 2.75, "description": "Good"},
        "CD": {"min": 55, "max": 59, "points": 2.5, "description": "Credit"},
        "D": {"min": 50, "max": 54, "points": 2.25, "description": "Credit"},
        "E": {"min": 45, "max": 49, "points": 2.0, "description": "Pass"},
        "F": {"min": 0, "max": 44, "points": 0.0, "description": "Fail"},
    }
    
    # Grading system uses credit load
    credit_unit_system: bool = True
    gpa_calculation = "weighted_by_credits"


def get_config(style: AcademicStyle = AcademicStyle.BRITISH_NIGERIAN,
               system_type: SystemType = SystemType.UNIVERSITY) -> UniversityConfig:
    """Get the appropriate configuration based on style and system type"""
    
    if system_type == SystemType.POLYTECHNIC:
        return PolytechnicConfig()
    
    if style == AcademicStyle.BRITISH_NIGERIAN:
        return BritishNigerianConfig()
    elif style == AcademicStyle.AMERICAN:
        return AmericanConfig()
    
    return UniversityConfig(academic_style=style, system_type=system_type)


def load_config_from_env() -> UniversityConfig:
    """Load configuration from environment variables"""
    
    style = os.getenv("ACADEMIC_STYLE", "british_nigerian")
    system_type = os.getenv("SYSTEM_TYPE", "university")
    
    style_enum = AcademicStyle(style) if style in [s.value for s in AcademicStyle] else AcademicStyle.BRITISH_NIGERIAN
    system_enum = SystemType(system_type) if system_type in [s.value for s in SystemType] else SystemType.UNIVERSITY
    
    return get_config(style_enum, system_enum)