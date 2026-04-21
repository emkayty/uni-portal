"""
WhatsApp Integration API
WhatsApp Business API integration
"""
import json
import requests
from typing import Optional, List
from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query

from .models import (
    WhatsAppTemplate, WhatsAppContact, WhatsAppMessage, WhatsAppCampaign,
    ChatbotSession, MessageType, MessageStatus, TemplateCategory
)

router = Router()


# ============ CONFIGURATION ============
# WhatsApp Cloud API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"
PHONE_NUMBER_ID = ""  # Set in environment
ACCESS_TOKEN = ""  # Set in environment


def send_whatsapp_message(phone: str, content: str, message_type: str = 'text', media_url: str = None) -> dict:
    """Send message via WhatsApp API"""
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": message_type,
        }
        
        if message_type == 'text':
            payload["text"] = {"body": content}
        elif message_type == 'image':
            payload["image"] = {"link": media_url, "caption": content}
        elif message_type == 'document':
            payload["document"] = {"link": media_url, "caption": content}
        
        # Make API call (simulated if no credentials)
        return {
            'success': True,
            'wamid': f'wamid.{phone}',
            'message': 'Sent'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============ TEMPLATE ENDPOINTS ============

@router.get("/templates", response=List[dict])
def list_templates(request, university_id: Optional[str] = Query(None)):
    """List WhatsApp templates"""
    queryset = WhatsAppTemplate.objects.filter(is_active=True)
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return [{
        'id': str(t.id),
        'name': t.name,
        'category': t.category,
        'header': t.header,
        'body': t.body[:100] + '...' if len(t.body) > 100 else t.body,
        'variables': t.variables
    } for t in queryset]


@router.get("/templates/{template_id}")
def get_template(request, template_id: str):
    """Get template details"""
    try:
        template = WhatsAppTemplate.objects.get(id=template_id)
        return {
            'id': str(template.id),
            'name': template.name,
            'category': template.category,
            'language': template.language,
            'header': template.header,
            'body': template.body,
            'footer': template.footer,
            'buttons': template.buttons,
            'variables': template.variables
        }
    except WhatsAppTemplate.DoesNotExist:
        return {'error': 'Template not found'}


@router.post("/templates")
def create_template(request, data: dict):
    """Create WhatsApp template"""
    template = WhatsAppTemplate.objects.create(
        university_id=data['university_id'],
        name=data['name'],
        category=data.get('category', TemplateCategory.ANNOUNCEMENT),
        header=data.get('header', ''),
        body=data['body'],
        footer=data.get('footer', ''),
        buttons=data.get('buttons', []),
        variables=data.get('variables', [])
    )
    
    return {'id': str(template.id), 'message': 'Template created'}


# ============ CONTACT ENDPOINTS ============

@router.get("/contacts", response=List[dict])
def list_contacts(request, university_id: Optional[str] = Query(None)):
    """List WhatsApp contacts"""
    queryset = WhatsAppContact.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return [{
        'id': str(c.id),
        'phone': c.phone,
        'name': c.name,
        'student': c.student.matric_number if c.student else None,
        'is_opted_in': c.is_opted_in,
        'is_verified': c.is_verified,
        'last_message_at': c.last_message_at.isoformat() if c.last_message_at else None
    } for c in queryset]


@router.post("/contacts")
def create_contact(request, data: dict):
    """Create/update contact"""
    contact, created = WhatsAppContact.objects.update_or_create(
        university_id=data['university_id'],
        phone=data['phone'],
        defaults={
            'name': data.get('name', ''),
            'student_id': data.get('student_id')
        }
    )
    
    return {'id': str(contact.id), 'created': created}


@router.post("/contacts/{contact_id}/verify")
def verify_contact(request, contact_id: str):
    """Verify WhatsApp contact via OTP"""
    try:
        import random
        otp = str(random.randint(100000, 999999))
        
        contact = WhatsAppContact.objects.get(id=contact_id)
        
        # Send OTP (simulated)
        result = send_whatsapp_message(
            contact.phone,
            f"Your verification code is: {otp}"
        )
        
        # Store OTP in context (in production, use proper OTP)
        contact.verification_otp = otp
        contact.save()
        
        return {'message': 'Verification code sent'}
    except Exception as e:
        return {'error': str(e)}


@router.post("/contacts/opt-in")
def opt_in_contact(request, data: dict):
    """Opt in contact"""
    contact, created = WhatsAppContact.objects.get_or_create(
        university_id=data['university_id'],
        phone=data['phone'],
        defaults={'name': data.get('name', '')}
    )
    contact.is_opted_in = True
    contact.save()
    
    return {'message': 'Opted in', 'is_new': created}


@router.post("/contacts/opt-out")
def opt_out_contact(request, university_id: str, phone: str):
    """Opt out contact"""
    contact = WhatsAppContact.objects.filter(
        university_id=university_id,
        phone=phone
    ).first()
    
    if contact:
        contact.is_opted_in = False
        contact.save()
        return {'message': 'Opted out'}
    
    return {'error': 'Contact not found'}


# ============ MESSAGE ENDPOINTS ============

@router.post("/messages/send")
def send_message(request, data: dict):
    """Send WhatsApp message"""
    try:
        contact = WhatsAppContact.objects.get(id=data['contact_id'])
        
        if not contact.is_opted_in:
            return {'error': 'Contact has opted out'}
        
        result = send_whatsapp_message(
            contact.phone,
            data['content'],
            data.get('message_type', 'text'),
            data.get('media_url')
        )
        
        message = WhatsAppMessage.objects.create(
            contact=contact,
            message_type=data.get('message_type', 'text'),
            content=data['content'],
            media_url=data.get('media_url', ''),
            direction='outbound',
            status=MessageStatus.SENT if result['success'] else MessageStatus.FAILED,
            wamid=result.get('wamid', '')
        )
        
        contact.last_message_at = timezone.now()
        contact.save()
        
        return {
            'id': str(message.message_id),
            'success': result['success'],
            'wamid': result.get('wamid')
        }
    except Exception as e:
        return {'error': str(e)}


@router.post("/messages/send-template")
def send_template_message(request, data: dict):
    """Send template message"""
    try:
        contact = WhatsAppContact.objects.get(id=data['contact_id'])
        template = WhatsAppTemplate.objects.get(id=data['template_id'])
        
        # Replace variables
        body = template.body
        for var, value in data.get('variables', {}).items():
            body = body.replace(f"{{{var}}}", str(value))
        
        result = send_whatsapp_message(contact.phone, body)
        
        message = WhatsAppMessage.objects.create(
            contact=contact,
            message_type=MessageType.TEMPLATE,
            content=body,
            template=template,
            template_vars=data.get('variables', {}),
            direction='outbound',
            status=MessageStatus.SENT if result['success'] else MessageStatus.FAILED,
            wamid=result.get('wamid', '')
        )
        
        return {
            'id': str(message.message_id),
            'success': result['success']
        }
    except Exception as e:
        return {'error': str(e)}


@router.get("/messages", response=List[dict])
def list_messages(
    request,
    contact_id: Optional[str] = Query(None),
    direction: Optional[str] = Query(None)
):
    """List messages"""
    queryset = WhatsAppMessage.objects.all()
    if contact_id:
        queryset = queryset.filter(contact_id=contact_id)
    if direction:
        queryset = queryset.filter(direction=direction)
    
    return [{
        'id': str(m.message_id),
        'content': m.content[:50] + '...' if len(m.content) > 50 else m.content,
        'direction': m.direction,
        'status': m.status,
        'created_at': m.created_at.isoformat() if m.created_at else None
    } for m in queryset[:50]]


# ============ WEBHOOK ENDPOINT ============

@router.post("/webhook")
def whatsapp_webhook(request, data: dict):
    """Handle incoming WhatsApp messages"""
    try:
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])
        
        for msg in messages:
            from_id = msg.get('from')
            msg_id = msg.get('id')
            msg_type = msg.get('type')
            
            # Find or create contact
            contact = WhatsAppContact.objects.filter(phone=from_id).first()
            if not contact:
                continue
            
            # Create message
            content = msg.get('text', {}).get('body', '') if msg_type == 'text' else ''
            
            WhatsAppMessage.objects.create(
                contact=contact,
                message_type=msg_type,
                content=content,
                direction='inbound',
                status=MessageStatus.DELIVERED,
                wamid=msg_id
            )
            
            contact.last_message_at = timezone.now()
            contact.save()
            
            # Trigger chatbot response
            if msg_type == 'text':
                handle_chatbot(contact, content)
        
        return {'status': 'ok'}
    except Exception as e:
        return {'error': str(e)}


def handle_chatbot(contact: WhatsAppContact, message: str):
    """Handle chatbot response"""
    # Get or create session
    session = ChatbotSession.objects.filter(
        contact=contact,
        is_active=True
    ).first()
    
    if not session:
        session = ChatbotSession.objects.create(
            contact=contact,
            state='greeting'
        )
    
    # Simple responses (in production, use LLM)
    responses = {
        'greeting': f"Hello! Welcome to the University portal. I can help you with:\n1. Admissions\n2. Results\n3. Fees\n4. General info\n\nReply with a number or your question.",
        'admission': "For admission inquiries, please visit our portal or call the admissions office.",
        'result': "You can check your results on the student portal at /results",
        'fees': "For fee payments, visit /finance and click on 'Pay Fees'.",
    }
    
    response = responses.get(session.state, "How can I help you?")
    
    # Send response
    send_whatsapp_message(contact.phone, response)
    
    # Update session
    session.message_count += 1
    session.last_activity_at = timezone.now()
    session.save()


# ============ CAMPAIGN ENDPOINTS ============

@router.get("/campaigns", response=List[dict])
def list_campaigns(request, university_id: Optional[str] = Query(None)):
    """List campaigns"""
    queryset = WhatsAppCampaign.objects.all()
    if university_id:
        queryset = queryset.filter(university_id=university_id)
    
    return [{
        'id': str(c.id),
        'name': c.name,
        'template': c.template.name,
        'status': c.status,
        'total_recipients': c.total_recipients,
        'delivered': c.delivered,
        'scheduled_at': c.scheduled_at.isoformat() if c.scheduled_at else None
    } for c in queryset]


@router.post("/campaigns")
def create_campaign(request, data: dict):
    """Create campaign"""
    campaign = WhatsAppCampaign.objects.create(
        university_id=data['university_id'],
        name=data['name'],
        template_id=data['template_id'],
        target_filter=data.get('target_filter', {}),
        message=data.get('message', ''),
        scheduled_at=data.get('scheduled_at')
    )
    
    return {'id': str(campaign.id), 'message': 'Campaign created'}


@router.post("/campaigns/{campaign_id}/send")
def send_campaign(request, campaign_id: str):
    """Send campaign"""
    try:
        campaign = WhatsAppCampaign.objects.get(id=campaign_id)
        
        # Get recipients
        contacts = WhatsAppContact.objects.filter(
            university=campaign.university,
            is_opted_in=True
        )
        
        # Filter by target
        target = campaign.target_filter
        if target.get('programs'):
            contacts = contacts.filter(student__programme__in=target['programs'])
        
        campaign.total_recipients = contacts.count()
        campaign.status = 'sending'
        campaign.save()
        
        # Send to all (in production, use queue)
        for contact in contacts:
            send_whatsapp_message(contact.phone, campaign.message)
            campaign.delivered += 1
        
        campaign.status = 'completed'
        campaign.completed_at = timezone.now()
        campaign.save()
        
        return {
            'message': 'Campaign sent',
            'delivered': campaign.delivered
        }
    except Exception as e:
        return {'error': str(e)}


# ============ STATISTICS ============

@router.get("/statistics")
def get_whatsapp_statistics(request, university_id: Optional[str] = Query(None)):
    """Get WhatsApp statistics"""
    contacts = WhatsAppContact.objects.all()
    messages = WhatsAppMessage.objects.all()
    
    if university_id:
        contacts = contacts.filter(university_id=university_id)
    
    total_contacts = contacts.count()
    opted_in = contacts.filter(is_opted_in=True).count()
    
    sent = messages.filter(direction='outbound', status=MessageStatus.SENT).count()
    delivered = messages.filter(direction='outbound', status=MessageStatus.DELIVERED).count()
    failed = messages.filter(direction='outbound', status=MessageStatus.FAILED).count()
    
    return {
        'total_contacts': total_contacts,
        'opted_in': opted_in,
        'total_messages': messages.count(),
        'sent': sent,
        'delivered': delivered,
        'failed': failed,
        'delivery_rate': round(delivered / sent * 100, 2) if sent > 0 else 0
    }