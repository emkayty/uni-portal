"""
Digital Credentials API
Blockchain-based credentials verification
"""
import hashlib
import json
from typing import Optional, List
from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query

from .models import (
    Credential, CredentialVerification, BlockchainRecord,
    CredentialType, CredentialStatus
)

router = Router()


# ============ CREDENTIAL ENDPOINTS ============

@router.get("/credentials", response=List[dict])
def list_credentials(
    request,
    student_id: Optional[str] = Query(None),
    credential_type: Optional[str] = Query(None)
):
    """List credentials"""
    queryset = Credential.objects.all()
    
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if credential_type:
        queryset = queryset.filter(credential_type=credential_type)
    
    return [{
        'id': str(c.credential_id),
        'credential_type': c.credential_type,
        'title': c.title,
        'issued_date': c.issued_date.isoformat() if c.issued_date else None,
        'expiry_date': c.expiry_date.isoformat() if c.expiry_date else None,
        'status': c.status,
        'verification_hash': c.verification_hash,
        'created_at': c.created_at.isoformat() if c.created_at else None
    } for c in queryset]


@router.get("/credentials/{credential_id}")
def get_credential(request, credential_id: str):
    """Get credential details"""
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        return {
            'id': str(credential.credential_id),
            'credential_type': credential.credential_type,
            'title': credential.title,
            'description': credential.description,
            'student': credential.student.matric_number,
            'student_name': str(credential.student.user.name) if credential.student.user else None,
            'issued_date': credential.issued_date.isoformat() if credential.issued_date else None,
            'expiry_date': credential.expiry_date.isoformat() if credential.expiry_date else None,
            'programme': credential.programme.name if credential.programme else None,
            'level': credential.level,
            'grade_classification': credential.grade_classification,
            'status': credential.status,
            'verification_hash': credential.verification_hash,
            'metadata': credential.metadata,
            'created_at': credential.created_at.isoformat() if credential.created_at else None
        }
    except Credential.DoesNotExist:
        return {'error': 'Credential not found'}


@router.post("/credentials")
def issue_credential(request, data: dict):
    """Issue a new credential"""
    try:
        from students.models import Student
        from university.models import Programme
        
        student = Student.objects.get(id=data['student_id'])
        programme = Programme.objects.get(id=data['programme_id']) if data.get('programme_id') else None
        
        credential = Credential.objects.create(
            student=student,
            credential_type=data['credential_type'],
            title=data['title'],
            description=data.get('description', ''),
            issued_date=data.get('issued_date', timezone.now().date()),
            expiry_date=data.get('expiry_date'),
            programme=programme,
            level=data.get('level', ''),
            grade_classification=data.get('grade_classification', ''),
            metadata=data.get('metadata', {}),
            issuing_authority_id=data.get('user_id')
        )
        
        # Generate verification hash
        credential.verification_hash = credential.generate_hash()
        credential.save()
        
        return {
            'id': str(credential.credential_id),
            'verification_hash': credential.verification_hash,
            'message': 'Credential issued successfully'
        }
    except Exception as e:
        return {'error': str(e)}


@router.post("/credentials/bulk")
def bulk_issue_credentials(request, data: dict):
    """Bulk issue credentials (e.g., for graduation)"""
    try:
        from students.models import Student
        from academic.models import Enrollment
        
        student_ids = data['student_ids']
        credential_type = data['credential_type']
        title = data['title']
        issued_date = data.get('issued_date', timezone.now().date())
        
        issued = []
        errors = []
        
        for student_id in student_ids:
            try:
                # Get student's completed programme
                student = Student.objects.get(id=student_id)
                enrollment = Enrollment.objects.filter(
                    student=student,
                    is_completed=True
                ).first()
                
                if not enrollment:
                    errors.append({'student_id': student_id, 'error': 'No completed enrollment'})
                    continue
                
                # Check if credential already exists
                existing = Credential.objects.filter(
                    student=student,
                    credential_type=credential_type,
                    title=title
                ).first()
                
                if existing:
                    errors.append({'student_id': student_id, 'error': 'Credential already exists'})
                    continue
                
                credential = Credential.objects.create(
                    student=student,
                    credential_type=credential_type,
                    title=title,
                    issued_date=issued_date,
                    programme=enrollment.course.programme if enrollment else None,
                    metadata=data.get('metadata', {})
                )
                
                credential.verification_hash = credential.generate_hash()
                credential.save()
                
                issued.append(str(credential.credential_id))
                
            except Exception as e:
                errors.append({'student_id': student_id, 'error': str(e)})
        
        return {
            'issued_count': len(issued),
            'error_count': len(errors),
            'issued': issued,
            'errors': errors
        }
    except Exception as e:
        return {'error': str(e)}


@router.get("/credentials/{credential_id}/verify")
def verify_credential(request, credential_id: str, verifier: str = '', email: str = ''):
    """Verify a credential"""
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        
        # Check expiry
        is_valid = credential.status == CredentialStatus.ISSUED
        if credential.expiry_date and credential.expiry_date < timezone.now().date():
            is_valid = False
        
        # Record verification
        ip = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        CredentialVerification.objects.create(
            credential=credential,
            verifier_name=verifier or 'Anonymous',
            verifier_email=email,
            ip_address=ip,
            user_agent=user_agent,
            result=is_valid
        )
        
        return {
            'valid': is_valid,
            'credential': {
                'id': str(credential.credential_id),
                'type': credential.credential_type,
                'title': credential.title,
                'student': credential.student.matric_number,
                'issued_date': credential.issued_date.isoformat() if credential.issued_date else None,
                'status': credential.status
            },
            'verified_at': timezone.now().isoformat()
        }
    except Credential.DoesNotExist:
        return {'valid': False, 'error': 'Credential not found'}


@router.get("/credentials/{credential_id}/verify-hash/{verification_hash}")
def verify_by_hash(request, credential_id: str, verification_hash: str):
    """Verify credential by hash"""
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        
        is_valid = (
            credential.verification_hash == verification_hash and
            credential.status == CredentialStatus.ISSUED
        )
        
        return {
            'valid': is_valid,
            'credential': {
                'id': str(credential.credential_id),
                'type': credential.credential_type,
                'title': credential.title,
                'student': credential.student.matric_number
            }
        }
    except Credential.DoesNotExist:
        return {'valid': False, 'error': 'Credential not found'}


@router.post("/credentials/{credential_id}/revoke")
def revoke_credential(request, credential_id: str, data: dict):
    """Revoke a credential"""
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        credential.status = CredentialStatus.REVOKED
        credential.metadata['revoked_reason'] = data.get('reason', '')
        credential.metadata['revoked_at'] = timezone.now().isoformat()
        credential.save()
        
        return {'message': 'Credential revoked'}
    except Credential.DoesNotExist:
        return {'error': 'Credential not found'}


@router.get("/credentials/{credential_id}/blockchain")
def get_blockchain_record(request, credential_id: str):
    """Get blockchain record for credential"""
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        record = credential.blockchain_record
        
        return {
            'network': record.network,
            'transaction_hash': record.transaction_hash,
            'block_number': record.block_number,
            'block_timestamp': record.block_timestamp.isoformat(),
            'contract_address': record.contract_address,
            'token_id': record.token_id,
            'metadata_uri': record.metadata_uri
        }
    except Credential.DoesNotExist:
        return {'error': 'Credential not found'}
    except BlockchainRecord.DoesNotExist:
        return {'error': 'No blockchain record'}


@router.post("/credentials/{credential_id}/blockchain")
def publish_to_blockchain(request, credential_id: str, data: dict):
    """Publish credential to blockchain"""
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        
        # Create blockchain record (simulated)
        record = BlockchainRecord.objects.create(
            credential=credential,
            network=data.get('network', 'ethereum'),
            transaction_hash=data.get('transaction_hash', ''),
            block_number=data.get('block_number', 0),
            block_timestamp=timezone.now(),
            contract_address=data.get('contract_address', ''),
            token_id=data.get('token_id', ''),
            metadata_uri=data.get('metadata_uri', '')
        )
        
        credential.blockchain_txid = data.get('transaction_hash', '')
        credential.save()
        
        return {
            'message': 'Published to blockchain',
            'transaction_hash': data.get('transaction_hash')
        }
    except Exception as e:
        return {'error': str(e)}


@router.get("/verifications")
def list_verifications(request, credential_id: Optional[str] = Query(None)):
    """List credential verifications"""
    queryset = CredentialVerification.objects.all()
    if credential_id:
        queryset = queryset.filter(credential_id=credential_id)
    
    return [{
        'verifier_name': v.verifier_name,
        'verifier_email': v.verifier_email,
        'verified_at': v.verified_at.isoformat() if v.verified_at else None,
        'result': v.result
    } for v in queryset[:50]]


@router.get("/statistics")
def get_credential_statistics(request):
    """Get credential statistics"""
    total = Credential.objects.count()
    issued = Credential.objects.filter(status=CredentialStatus.ISSUED).count()
    revoked = Credential.objects.filter(status=CredentialStatus.REVOKED).count()
    verified = CredentialVerification.objects.count()
    
    by_type = {}
    for ct in CredentialType:
        count = Credential.objects.filter(credential_type=ct.value).count()
        by_type[ct.value] = count
    
    return {
        'total': total,
        'issued': issued,
        'revoked': revoked,
        'total_verifications': verified,
        'by_type': by_type
    }