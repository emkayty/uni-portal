"""
Finance API Endpoints
Invoices, payments, fees, scholarships, TETFund
"""
import uuid
from ninja import Router, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime

router = Router()


# === SCHEMAS ===

class FeeTypeSchema(BaseModel):
    id: Optional[str] = None
    name: str
    university_id: str
    category: str  # tuition, academic, hostel, medical, etc.
    amount: float
    applicable_levels: List[int] = []
    is_mandatory: bool = True
    is_recurring: bool = True
    tetfund_levy: bool = False
    tetfund_percentage: float = 0
    
    class Config:
        from_attributes = True


class InvoiceSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    semester_id: str
    invoice_number: str
    total_amount: float
    paid_amount: float = 0
    balance: float = 0
    status: str = "draft"  # draft, issued, partial, paid, overdue
    issue_date: date
    due_date: date
    
    class Config:
        from_attributes = True


class InvoiceItemSchema(BaseModel):
    id: Optional[str] = None
    invoice_id: str
    fee_type_id: str
    description: str
    amount: float
    
    class Config:
        from_attributes = True


class PaymentSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    invoice_id: Optional[str] = None
    payment_reference: str
    amount: float
    payment_method: str  # remita, paystack, flutterwave, bank_transfer, ussd
    status: str = "pending"  # pending, processing, completed, failed
    gateway_reference: str = ""
    remita_rrr: str = ""
    paystack_ref: str = ""
    bank_name: str = ""
    transaction_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InstallmentSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    semester_id: str
    installment_number: int
    amount: float
    due_date: date
    paid_date: Optional[date] = None
    status: str = "pending"  # pending, paid, overdue
    
    class Config:
        from_attributes = True


class ScholarshipSchema(BaseModel):
    id: Optional[str] = None
    name: str
    university_id: str
    scholarship_type: str  # tetfund, federal, state, institutional, external
    description: str
    amount: float
    number_of_awards: int
    eligible_levels: List[int] = []
    eligible_programmes: List[str] = []
    min_cgpa: float = 0
    application_start: date
    application_end: date
    status: str = "open"  # open, closed, review, awarded
    provider_name: str = ""
    
    class Config:
        from_attributes = True


class ScholarshipApplicationSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    scholarship_id: str
    status: str = "pending"  # pending, screening, shortlisted, approved, rejected
    amount_awarded: Optional[float] = None
    notes: str = ""
    
    class Config:
        from_attributes = True


# === ENDPOINTS ===

# --- FEE TYPES ---

@router.get("/fee-types", )
def list_fee_types(request, 
    university_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    """List fee types"""
    from finance.models import FeeType
    queryset = FeeType.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    if category:
        queryset = queryset.filter(category=category)
    return [
        {
            "id": str(q.id),
            "name": q.name,
            "category": q.category,
            "amount": float(q.amount),
            "is_mandatory": q.is_mandatory,
        }
        for q in queryset
    ]


@router.post("/fee-types")
def create_fee_type(request, data: FeeTypeSchema):
    """Create a new fee type"""
    from finance.models import FeeType, University
    uni = University.objects.get(id=data.university_id)
    fee = FeeType.objects.create(
        university=uni,
        name=data.name,
        category=data.category,
        amount=data.amount,
        applicable_levels=data.applicable_levels,
        is_mandatory=data.is_mandatory,
        is_recurring=data.is_recurring,
        tetfund_levy=data.tetfund_levy,
        tetfund_percentage=data.tetfund_percentage,
    )
    return fee


# --- INVOICES ---

@router.get("/invoices")
def list_invoices(request, 
    student_id: Optional[str] = Query(None),
    semester_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List invoices"""
    from finance.models import Invoice
    queryset = Invoice.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if semester_id:
        queryset = queryset.filter(semester_id=semester_id)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(q.id),
            "student": str(q.student.user.name) if q.student else None,
            "semester": q.semester.name if q.semester else None,
            "amount": float(q.amount),
            "status": q.status,
            "created_at": str(q.created_at) if q.created_at else None,
        }
        for q in queryset
    ]


@router.post("/invoices")
def create_invoice(request, data: InvoiceSchema):
    """Create a new invoice"""
    from finance.models import Invoice
    student = Student.objects.get(id=data.student_id)
    semester = Semester.objects.get(id=data.semester_id)
    invoice = Invoice.objects.create(
        student=student,
        semester=semester,
        invoice_number=data.invoice_number,
        total_amount=data.total_amount,
        paid_amount=data.paid_amount,
        balance=data.balance,
        status=data.status,
        issue_date=data.issue_date,
        due_date=data.due_date,
    )
    return invoice


@router.get("/invoices/{invoice_id}")
def get_invoice(request, invoice_id: str):
    """Get invoice details with items"""
    from finance.models import Invoice, InvoiceItem
    invoice = Invoice.objects.get(id=invoice_id)
    items = InvoiceItem.objects.filter(invoice=invoice)
    return {
        "invoice": {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "student": invoice.student.student_id,
            "total_amount": float(invoice.total_amount),
            "paid_amount": float(invoice.paid_amount),
            "balance": float(invoice.balance),
            "status": invoice.status,
            "issue_date": invoice.issue_date,
            "due_date": invoice.due_date,
        },
        "items": [
            {
                "fee_type": item.fee_type.name,
                "description": item.description,
                "amount": float(item.amount),
            }
            for item in items
        ]
    }


@router.get("/invoices/student/{student_id}/current")
def get_current_invoice(request, student_id: str):
    """Get current invoice for a student"""
    from finance.models import Invoice
    
    # Get current semester
    current_sem = Semester.objects.filter(is_active=True).first()
    if not current_sem:
        return {"error": "No active semester"}
    
    invoice = Invoice.objects.filter(
        student_id=student_id,
        semester=current_sem
    ).first()
    
    if not invoice:
        return {"error": "No invoice found"}
    
    return {
        "invoice_number": invoice.invoice_number,
        "total_amount": float(invoice.total_amount),
        "paid_amount": float(invoice.paid_amount),
        "balance": float(invoice.balance),
        "status": invoice.status,
        "due_date": invoice.due_date,
    }


@router.post("/invoices/{invoice_id}/generate")
def generate_student_invoice(invoice_id: str):
    """Generate invoice for a student (creates line items)"""
    from finance.models import Invoice, FeeType
    from students.models import User
    
    invoice = Invoice.objects.get(id=invoice_id)
    student = invoice.student
    semester = invoice.semester
    
    # Get applicable fee types
    fee_types = FeeType.objects.filter(
        university=student.university,
        is_active=True
    ).filter(
        applicable_levels__contains=[student.level]
    )
    
    for ft in fee_types:
        # Calculate TETFund levy if applicable
        amount = ft.amount
        if ft.tetfund_levy:
            levy_amount = amount * (ft.tetfund_percentage / 100)
            # Create levy item
            InvoiceItem.objects.create(
                invoice=invoice,
                fee_type=ft,
                description=f"TETFund Levy ({ft.tetfund_percentage}%)",
                amount=levy_amount,
            )
            amount += levy_amount
        
        InvoiceItem.objects.create(
            invoice=invoice,
            fee_type=ft,
            description=ft.name,
            amount=amount,
        )
    
    # Update invoice total
    total = sum(item.amount for item in InvoiceItem.objects.filter(invoice=invoice))
    invoice.total_amount = total
    invoice.balance = total
    invoice.status = "issued"
    invoice.save()
    
    return {
        "status": "generated",
        "items": InvoiceItem.objects.filter(invoice=invoice).count(),
        "total": float(invoice.total_amount)
    }


# --- PAYMENTS ---

@router.get("/payments")
def list_payments(request, 
    student_id: Optional[str] = Query(None),
    invoice_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List payments"""
    from finance.models import Payment
    queryset = Payment.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if invoice_id:
        queryset = queryset.filter(invoice_id=invoice_id)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(q.id),
            "student": str(q.student.user.name) if q.student else None,
            "amount": float(q.amount),
            "method": q.payment_method,
            "status": q.status,
            "date": str(q.payment_date) if q.payment_date else None,
        }
        for q in queryset
    ]


@router.post("/payments")
def create_payment(request, data: PaymentSchema):
    """Record a new payment"""
    from finance.models import Payment
    student = Student.objects.get(id=data.student_id)
    
    invoice = None
    if data.invoice_id:
        invoice = Invoice.objects.get(id=data.invoice_id)
    
    payment = Payment.objects.create(
        student=student,
        invoice=invoice,
        payment_reference=data.payment_reference,
        amount=data.amount,
        payment_method=data.payment_method,
        status=data.status,
        gateway_reference=data.gateway_reference,
        remita_rrr=data.remita_rrr,
        paystack_ref=data.paystack_ref,
        bank_name=data.bank_name,
        transaction_date=data.transaction_date,
    )
    return payment


@router.post("/payments/{payment_id}/confirm")
def confirm_payment(payment_id: str):
    """Confirm a payment and update invoice"""
    from finance.models import Payment, Invoice
    
    payment = Payment.objects.get(id=payment_id)
    payment.status = "completed"
    payment.save()
    
    # Update invoice if linked
    if payment.invoice:
        invoice = payment.invoice
        invoice.paid_amount += payment.amount
        invoice.calculate_balance()
        
        return {
            "status": "confirmed",
            "payment_reference": payment.payment_reference,
            "invoice_balance": float(invoice.balance),
            "invoice_status": invoice.status,
        }
    
    return {
        "status": "confirmed",
        "payment_reference": payment.payment_reference,
    }


@router.post("/payments/remita/verify")
def verify_remita_payment(rrr: str):
    """Verify payment via Remita"""
    # In production, call Remita API
    # For demo, return success
    return {
        "rrr": rrr,
        "status": "paid",
        "amount": 150000.00,
        "date": datetime.now().isoformat(),
    }


@router.post("/payments/paystack/verify")
def verify_paystack_payment(reference: str):
    """Verify payment via Paystack"""
    # In production, call Paystack API
    return {
        "reference": reference,
        "status": "success",
        "amount": 150000.00,
    }


# --- INSTALLMENTS ---

@router.get("/installments")
def list_installments(request, 
    student_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List installments"""
    from finance.models import Installment
    queryset = Installment.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(q.id),
            "student": str(q.student.user.name) if q.student else None,
            "amount": float(q.amount),
            "due_date": str(q.due_date) if q.due_date else None,
            "status": q.status,
        }
        for q in queryset
    ]


@router.post("/installments")
def create_installment(request, data: InstallmentSchema):
    """Create installment plan"""
    from finance.models import Installment
    student = Student.objects.get(id=data.student_id)
    semester = Semester.objects.get(id=data.semester_id)
    
    installment = Installment.objects.create(
        student=student,
        semester=semester,
        installment_number=data.installment_number,
        amount=data.amount,
        due_date=data.due_date,
        status=data.status,
    )
    return installment


@router.get("/installments/student/{student_id}/current")
def get_student_installments(student_id: str):
    """Get current installments for a student"""
    from finance.models import Installment
    
    current_sem = Semester.objects.filter(is_active=True).first()
    if not current_sem:
        return {"error": "No active semester"}
    
    installments = Installment.objects.filter(
        student_id=student_id,
        semester=current_sem
    ).order_by('installment_number')
    
    return {
        "installments": [
            {
                "number": i.installment_number,
                "amount": float(i.amount),
                "due_date": i.due_date,
                "paid_date": i.paid_date,
                "status": i.status,
            }
            for i in installments
        ]
    }


# --- SCHOLARSHIPS ---

@router.get("/scholarships")
def list_scholarships(request, 
    university_id: Optional[str] = Query(None),
    scholarship_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List scholarships"""
    from finance.models import Scholarship
    queryset = Scholarship.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    if scholarship_type:
        queryset = queryset.filter(scholarship_type=scholarship_type)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(q.id),
            "name": q.name,
            "amount": float(q.amount),
            "type": q.scholarship_type,
            "criteria": q.eligibility_criteria,
        }
        for q in queryset
    ]


@router.post("/scholarships")
def create_scholarship(request, data: ScholarshipSchema):
    """Create a new scholarship"""
    from finance.models import Scholarship
    uni = University.objects.get(id=data.university_id)
    scholarship = Scholarship.objects.create(
        university=uni,
        name=data.name,
        scholarship_type=data.scholarship_type,
        description=data.description,
        amount=data.amount,
        number_of_awards=data.number_of_awards,
        eligible_levels=data.eligible_levels,
        eligible_programmes=data.eligible_programmes,
        min_cgpa=data.min_cgpa,
        application_start=data.application_start,
        application_end=data.application_end,
        status=data.status,
        provider_name=data.provider_name,
    )
    return scholarship


@router.get("/scholarships/available")
def get_available_scholarships(student_id: str):
    """Get scholarships a student is eligible for"""
    from finance.models import Scholarship
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    
    # Find open scholarships matching criteria
    scholarships = Scholarship.objects.filter(
        university=student.university,
        status="open",
        eligible_levels__contains=[student.level]
    )
    
    results = []
    for s in scholarships:
        # Check if already applied
        from finance.models import ScholarshipApplication
        applied = ScholarshipApplication.objects.filter(
            student=student,
            scholarship=s
        ).exists()
        
        results.append({
            "id": s.id,
            "name": s.name,
            "type": s.scholarship_type,
            "amount": float(s.amount),
            "min_cgpa": s.min_cgpa,
            "deadline": s.application_end,
            "already_applied": applied,
        })
    
    return results


# --- SCHOLARSHIP APPLICATIONS ---

@router.get("/scholarship-applications")
def list_scholarship_applications(request, 
    student_id: Optional[str] = Query(None),
    scholarship_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List scholarship applications"""
    from finance.models import ScholarshipApplication
    queryset = ScholarshipApplication.objects.all()
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if scholarship_id:
        queryset = queryset.filter(scholarship_id=scholarship_id)
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(q.id),
            "student": str(q.student.user.name) if q.student else None,
            "scholarship": q.scholarship.name if q.scholarship else None,
            "status": q.status,
            "applied_at": str(q.applied_at) if q.applied_at else None,
        }
        for q in queryset
    ]


@router.post("/scholarship-applications")
def apply_for_scholarship(data: ScholarshipApplicationSchema):
    """Apply for a scholarship"""
    from finance.models import ScholarshipApplication
    
    student = Student.objects.get(id=data.student_id)
    scholarship = Scholarship.objects.get(id=data.scholarship_id)
    
    # Check eligibility
    if student.level not in scholarship.eligible_levels:
        return {"error": "Not eligible for this scholarship"}
    
    application = ScholarshipApplication.objects.create(
        student=student,
        scholarship=scholarship,
        status=data.status,
        notes=data.notes,
    )
    return application


# --- FINANCIAL REPORTS ---

@router.get("/reports/student/{student_id}/summary")
def get_student_financial_summary(student_id: str):
    """Get student financial summary"""
    from finance.models import Invoice, Payment, Installment
    from students.models import Student
    
    student = Student.objects.get(id=student_id)
    
    # Total invoiced
    total_invoiced = sum(
        float(i.total_amount) for i in Invoice.objects.filter(student=student)
    )
    
    # Total paid
    total_paid = sum(
        float(p.amount) for p in Payment.objects.filter(student=student, status="completed")
    )
    
    # Outstanding
    outstanding = total_invoiced - total_paid
    
    # Pending installments
    pending_installments = Installment.objects.filter(
        student=student,
        status="pending"
    ).count()
    
    return {
        "student_id": student.student_id,
        "total_invoiced": total_invoiced,
        "total_paid": total_paid,
        "outstanding": outstanding,
        "pending_installments": pending_installments,
    }


@router.get("/reports/university/{university_id}/revenue")
def get_university_revenue(university_id: str):
    """Get university revenue report"""
    from finance.models import Payment, Invoice
    from university.models import University
    
    uni = University.objects.get(id=university_id)
    
    # Get payments for current year
    payments = Payment.objects.filter(
        student__university=uni,
        status="completed"
    )
    
    total_revenue = sum(float(p.amount) for p in payments)
    
    return {
        "university": uni.short_name,
        "total_revenue": total_revenue,
        "payment_count": payments.count(),
    }


# ============= HOSTEL BOOKING =============
HOSTEL_APPLICATIONS = []


class HostelApplicationRequest(BaseModel):
    student_id: str
    hostel_id: str
    room_type: str = Field(..., description="single, double, triple")
    semester_id: str


@router.post("/hostel/apply")
def apply_for_hostel(request, data: HostelApplicationRequest):
    """Apply for hostel accommodation"""
    app = {
        "id": f"hostel-app-{len(HOSTEL_APPLICATIONS)+1}",
        "student_id": data.student_id,
        "hostel_id": data.hostel_id,
        "room_type": data.room_type,
        "semester_id": data.semester_id,
        "status": "pending",
        "applied_at": "2024-01-15"
    }
    HOSTEL_APPLICATIONS.append(app)
    return {"success": True, "application": app}


@router.get("/hostel/applications/student/{student_id}")
def get_student_hostel_applications(request, student_id: str):
    """Get student's hostel applications"""
    apps = [a for a in HOSTEL_APPLICATIONS if a["student_id"] == student_id]
    return {"student_id": student_id, "applications": apps}


@router.post("/hostel/applications/{application_id}/approve")
def approve_hostel_application(request, application_id: str):
    """Approve hostel application"""
    app = next((a for a in HOSTEL_APPLICATIONS if a["id"] == application_id), None)
    if not app:
        return {"error": "Application not found"}
    app["status"] = "approved"
    return {"success": True, "application": app}


# ============= TRANSCRIPT REQUEST =============
TRANSCRIPT_REQUESTS = []


class TranscriptRequestSchema(BaseModel):
    student_id: str
    transcript_type: str = Field(..., description="official, unofficial")
    delivery_method: str = Field(..., description="pickup, email, courier")
    recipient_name: Optional[str] = None
    recipient_address: Optional[str] = None


@router.post("/transcript/request")
def request_transcript(request, data: TranscriptRequestSchema):
    """Request academic transcript"""
    req = {
        "id": f"trans-{len(TRANSCRIPT_REQUESTS)+1}",
        "student_id": data.student_id,
        "transcript_type": data.transcript_type,
        "delivery_method": data.delivery_method,
        "status": "pending",
        "requested_at": "2024-01-15",
        "processing_time_days": 3
    }
    TRANSCRIPT_REQUESTS.append(req)
    return {"success": True, "request": req, "message": "Transcript request submitted"}


@router.get("/transcript/requests/student/{student_id}")
def get_student_transcript_requests(request, student_id: str):
    """Get student's transcript requests"""
    reqs = [r for r in TRANSCRIPT_REQUESTS if r["student_id"] == student_id]
    return {"student_id": student_id, "requests": reqs}


@router.get("/transcript/{request_id}")
def get_transcript_request(request, request_id: str):
    """Get transcript request status"""
    req = next((r for r in TRANSCRIPT_REQUESTS if r["id"] == request_id), None)
    if not req:
        return {"error": "Request not found"}
    return req


# ============= NOTIFICATION SERVICE =============
NOTIFICATIONS = []


class NotificationRequest(BaseModel):
    recipient_id: str
    channel: str = Field(..., description="email, sms, whatsapp")
    subject: Optional[str] = None
    message: str
    priority: str = "normal"  # low, normal, high


@router.post("/notifications/send")
def send_notification(request, data: NotificationRequest):
    """Send notification (email/SMS/WhatsApp)"""
    notification = {
        "id": f"notif-{len(NOTIFICATIONS)+1}",
        "recipient_id": data.recipient_id,
        "channel": data.channel,
        "subject": data.subject or "",
        "message": data.message,
        "priority": data.priority,
        "status": "sent",
        "sent_at": "2024-01-15"
    }
    NOTIFICATIONS.append(notification)
    return {"success": True, "notification": notification}


@router.get("/notifications/student/{student_id}")
def get_student_notifications(request, student_id: str):
    """Get student's notifications"""
    notifs = [n for n in NOTIFICATIONS if n["recipient_id"] == student_id]
    return {"student_id": student_id, "notifications": notifs}


@router.post("/notifications/bulk")
def send_bulk_notifications(request, recipient_ids: List[str], channel: str, message: str):
    """Send bulk notifications"""
    results = []
    for recipient_id in recipient_ids:
        notification = {
            "id": f"notif-{len(NOTIFICATIONS)+1}",
            "recipient_id": recipient_id,
            "channel": channel,
            "message": message,
            "status": "sent"
        }
        NOTIFICATIONS.append(notification)
        results.append(notification)
    return {"success": True, "sent_count": len(results), "notifications": results}


# ============= REAL-TIME CONFIG =============
@router.get("/realtime/config")
def get_realtime_config(request):
    """Get real-time notification configuration"""
    return {
        "centrifugo_url": os.environ.get("CENTRIFUGO_URL", "ws://localhost:8000"),
        "websocket_enabled": True,
        "notification_types": ["grade", "payment", "attendance", "announcement"],
        "push_enabled": True
    }