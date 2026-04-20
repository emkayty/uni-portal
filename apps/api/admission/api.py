"""
Admission API Endpoints
CAPS integration, JAMB data, applications, screening
"""
from typing import Optional, List
from ninja import Router, Query
from pydantic import BaseModel

router = Router()


# === SCHEMAS ===

class AdmissionApplicationOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    jamb_registration_number: str
    jamb_score: int
    status: str
    post_utme_score: Optional[int] = None

    class Config:
        from_attributes = True


class AdmissionBatchOut(BaseModel):
    id: str
    name: str
    academic_year: str
    session: str
    application_deadline: Optional[str] = None
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


class CAPSDataImportOut(BaseModel):
    id: str
    jamb_registration: str
    candidate_name: str
    date_of_birth: Optional[str] = None
    state_origin: Optional[str] = None
    lga: Optional[str] = None
    exam_year: Optional[int] = None
    exam_center: Optional[str] = None
    imported_at: str

    class Config:
        from_attributes = True


# === ADMISSION APPLICATION ENDPOINTS ===

@router.get("/applications", response=List[AdmissionApplicationOut])
def list_admission_applications(request, status: Optional[str] = Query(None)):
    """List all admission applications with optional status filter"""
    from admission.models import AdmissionApplication
    queryset = AdmissionApplication.objects.all()
    if status:
        queryset = queryset.filter(status=status)
    return [
        {
            "id": str(a.id),
            "first_name": a.first_name,
            "last_name": a.last_name,
            "email": a.email,
            "jamb_registration_number": a.jamb_registration_number,
            "jamb_score": a.jamb_score,
            "status": a.status,
            "post_utme_score": a.post_utme_score,
        }
        for a in queryset
    ]


@router.get("/applications/{application_id}", response=AdmissionApplicationOut)
def get_admission_application(request, application_id: str):
    """Get a specific admission application"""
    from admission.models import AdmissionApplication
    a = AdmissionApplication.objects.get(id=application_id)
    return {
        "id": str(a.id),
        "first_name": a.first_name,
        "last_name": a.last_name,
        "email": a.email,
        "jamb_registration_number": a.jamb_registration_number,
        "jamb_score": a.jamb_score,
        "status": a.status,
        "post_utme_score": a.post_utme_score,
    }


@router.get("/caps/candidates", response=List[CAPSDataImportOut])
def list_caps_candidates(request, batch: Optional[str] = Query(None)):
    """List CAPS imported candidates"""
    from admission.models import CAPSDataImport
    queryset = CAPSDataImport.objects.all()
    return [
        {
            "id": str(c.id),
            "jamb_registration": c.jamb_registration,
            "candidate_name": c.candidate_name,
            "date_of_birth": str(c.date_of_birth) if c.date_of_birth else None,
            "state_origin": c.state_origin,
            "lga": c.lga,
            "exam_year": c.exam_year,
            "exam_center": c.exam_center,
            "imported_at": c.imported_at.isoformat() if c.imported_at else None,
        }
        for c in queryset
    ]


@router.get("/batches", response=List[AdmissionBatchOut])
def list_admission_batches(request, active_only: bool = Query(False)):
    """List admission batches"""
    from admission.models import AdmissionBatch
    queryset = AdmissionBatch.objects.all()
    if active_only:
        queryset = queryset.filter(is_active=True)
    return [
        {
            "id": str(b.id),
            "name": b.name,
            "academic_year": b.academic_year,
            "session": b.session,
            "application_deadline": b.application_deadline.isoformat() if b.application_deadline else None,
            "is_active": b.is_active,
            "created_at": b.created_at.isoformat() if b.created_at else None,
        }
        for b in queryset
    ]


@router.get("/statistics")
def admission_statistics(request):
    """Get admission statistics"""
    from admission.models import AdmissionApplication, AdmissionBatch
    
    total_applications = AdmissionApplication.objects.count()
    admitted = AdmissionApplication.objects.filter(status='offered').count()
    pending = AdmissionApplication.objects.filter(status='submitted').count()
    rejected = AdmissionApplication.objects.filter(status='rejected').count()
    active_batches = AdmissionBatch.objects.filter(is_active=True).count()
    
    return {
        "total_applications": total_applications,
        "admitted": admitted,
        "pending": pending,
        "rejected": rejected,
        "active_batches": active_batches,
        "acceptance_rate": round(admitted / total_applications * 100, 2) if total_applications > 0 else 0,
    }


@router.post("/applications/{application_id}/offer")
def offer_admission(request, application_id: str):
    """Offer admission to a candidate"""
    from admission.models import AdmissionApplication
    app = AdmissionApplication.objects.get(id=application_id)
    app.status = 'offered'
    app.save()
    return {"status": "success", "application_id": str(app.id), "new_status": app.status}


@router.post("/applications/{application_id}/reject")
def reject_admission(request, application_id: str):
    """Reject an application"""
    from admission.models import AdmissionApplication
    app = AdmissionApplication.objects.get(id=application_id)
    app.status = 'rejected'
    app.save()
    return {"status": "success", "application_id": str(app.id), "new_status": app.status}