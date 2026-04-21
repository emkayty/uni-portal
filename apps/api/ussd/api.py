"""
USSD API
Unstructured Supplementary Service Data
"""
import uuid
import time
from typing import Optional, List

from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query

from .models import UssdMenu, UssdSession, UssdLog

router = Router()


# ============ DEFAULT MENUS ============
DEFAULT_MENUS = {
    'main': {
        '1': ('Check Result', 'check_result'),
        '2': ('Check Fees', 'check_fees'),
        '3': ('Course Registration', 'course_reg'),
        '4': ('Check Profile', 'check_profile'),
        '5': ('Hostel Status', 'hostel_status'),
        '0': ('Exit', 'exit')
    },
    'check_result': {
        '1': ('View Last Result', 'view_last_result'),
        '2': ('View All Results', 'view_all_results'),
        '0': ('Back', 'main')
    },
    'check_fees': {
        '1': ('Check Balance', 'check_balance'),
        '2': ('Pay Fees', 'pay_fees'),
        '0': ('Back', 'main')
    },
    'check_profile': {
        '1': ('View Profile', 'view_profile'),
        '2': ('Update Contact', 'update_contact'),
        '0': ('Back', 'main')
    }
}


def build_menu_text(menu_key: str, menu_tree: dict = None) -> str:
    """Build USSD menu text"""
    tree = menu_tree or DEFAULT_MENUS
    
    if menu_key not in tree:
        return "Invalid option. Thank you."
    
    menu = tree[menu_key]
    lines = []
    
    for key, (label, _) in menu.items():
        lines.append(f"{key}. {label}")
    
    return "\n".join(lines)


def get_student_by_phone(phone: str, university_id: str):
    """Get student by phone number"""
    from students.models import Student
    from whatsapp.models import WhatsAppContact
    
    # Try WhatsApp contact first
    contact = WhatsAppContact.objects.filter(
        phone=phone,
        university_id=university_id,
        is_verified=True
    ).first()
    
    if contact and contact.student:
        return contact.student
    
    # Try direct student lookup
    student = Student.objects.filter(
        phone__endswith=phone[-10:]
    ).first()
    
    return student


# ============ MENU ENDPOINTS ============

@router.get("/menus", response=List[dict])
def list_ussd_menus(request, university_id: Optional[str] = Query(None)):
    """List USSD menus"""
    queryset = UssdMenu.objects.filter(is_active=True)
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return [{
        'id': str(m.id),
        'name': m.name,
        'code': m.code,
        'entry_point': m.entry_point,
        'is_active': m.is_active
    } for m in queryset]


@router.post("/menus")
def create_ussd_menu(request, data: dict):
    """Create USSD menu"""
    menu = UssdMenu.objects.create(
        university_id=data['university_id'],
        name=data['name'],
        code=data['code'],
        menu_tree=data.get('menu_tree', DEFAULT_MENUS)
    )
    
    return {'id': str(menu.id), 'message': 'USSD menu created'}


# ============ USSD SESSION ENDPOINTS ============

@router.post("/session")
def handle_ussd(request, data: dict):
    """Handle USSD session"""
    start_time = time.time()
    
    phone = data.get('phone', '')
    text = data.get('text', '')
    university_id = data.get('university_id', '')
    
    # Parse input
    inputs = text.split('*')[-1].split('#')[0].split('*') if text else ['']
    current_input = inputs[-1] if inputs else ''
    
    # Get or create session
    session_id = data.get('session_id')
    if session_id:
        session = UssdSession.objects.filter(session_id=session_id).first()
    else:
        session = None
    
    # Check if new session
    if not session or not session.is_active:
        # Create new session
        session = UssdSession.objects.create(
            session_id=str(uuid.uuid4()),
            phone=phone,
            university_id=university_id,
            current_menu='main',
            is_active=True
        )
        response = build_menu_text('main')
        
        return {
            'session_id': session.session_id,
            'response': response,
            'continue': True
        }
    
    # Process input
    menu = session.current_menu
    menu_tree = DEFAULT_MENUS
    
    # Get menu options
    if menu in menu_tree:
        options = menu_tree[menu]
        
        if current_input == '0':
            # Go back
            if session.previous_menu:
                session.current_menu = session.previous_menu
                session.previous_menu = ''
            else:
                session.current_menu = 'main'
            session.save()
            response = build_menu_text(session.current_menu)
        elif current_input in options:
            # Process selection
            _, next_menu = options[current_input]
            
            if next_menu == 'exit':
                session.is_active = False
                session.ended_at = timezone.now()
                session.save()
                
                # Log
                UssdLog.objects.create(
                    session=session,
                    menu=menu,
                    user_input=current_input,
                    response="Thank you for using our service.",
                    duration_ms=int((time.time() - start_time) * 1000)
                )
                
                return {
                    'session_id': session.session_id,
                    'response': "Thank you for using our service.",
                    'continue': False
                }
            
            # Save previous and go to next
            session.previous_menu = menu
            session.current_menu = next_menu
            session.save()
            
            # Get response based on menu
            response = get_menu_response(next_menu, current_input, session)
        else:
            response = "Invalid option. " + build_menu_text(session.current_menu)
    else:
        response = build_menu_text('main')
        session.current_menu = 'main'
        session.save()
    
    # Log the interaction
    UssdLog.objects.create(
        session=session,
        menu=menu,
        user_input=current_input,
        response=response,
        duration_ms=int((time.time() - start_time) * 1000)
    )
    
    return {
        'session_id': session.session_id,
        'response': response,
        'continue': True
    }


def get_menu_response(menu: str, input_data: str, session: UssdSession) -> str:
    """Get dynamic menu response"""
    
    if menu == 'view_last_result':
        # Get last result
        try:
            from academic.models import Enrollment
            enrollment = Enrollment.objects.filter(
                student=session.student
            ).first()
            
            if enrollment:
                return f"Your last result:\n{enrollment.course.code}: {enrollment.grade or 'Pending'}"
            return "No results found."
        except:
            return "Please register on the portal first."
    
    elif menu == 'check_balance':
        try:
            from finance.models import Invoice
            invoices = Invoice.objects.filter(
                student=session.student,
                status__in=['pending', 'overdue']
            )
            total = sum(float(i.amount) for i in invoices)
            return f"Your outstanding balance: ₦{total:,.2f}"
        except:
            return "Unable to check balance."
    
    elif menu == 'view_profile':
        if session.student:
            return f"Name: {session.student.user.name}\nMatric: {session.student.matric_number}"
        return "Profile not found."
    
    else:
        return build_menu_text(menu)


@router.get("/sessions")
def list_ussd_sessions(request, phone: Optional[str] = Query(None)):
    """List USSD sessions"""
    queryset = UssdSession.objects.all()
    if phone:
        queryset = queryset.filter(phone=phone)
    
    return [{
        'id': str(s.id),
        'phone': s.phone,
        'current_menu': s.current_menu,
        'is_active': s.is_active,
        'started_at': s.started_at.isoformat() if s.started_at else None
    } for s in queryset[:50]]


# ============ STATISTICS ============

@router.get("/statistics")
def get_ussd_statistics(request, university_id: Optional[str] = Query(None)):
    """Get USSD statistics"""
    sessions = UssdSession.objects.all()
    logs = UssdLog.objects.all()
    
    if university_id:
        sessions = sessions.filter(university_id=university_id)
    
    total_sessions = sessions.count()
    active_sessions = sessions.filter(is_active=True).count()
    completed_sessions = sessions.filter(is_active=False).count()
    
    # Average session duration
    avg_duration = 0
    completed = logs.filter(duration_ms__isnull=False)
    if completed.exists():
        avg_duration = completed.aggregate(avg=Avg('duration_ms'))['avg'] or 0
    
    return {
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'completed_sessions': completed_sessions,
        'total_requests': logs.count(),
        'avg_duration_ms': round(avg_duration, 2)
    }