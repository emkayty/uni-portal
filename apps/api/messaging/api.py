"""
Messaging API Endpoints
Announcements, notifications, messages, alerts
"""
from typing import Optional, List
from ninja import Router, Query
from pydantic import BaseModel

router = Router()


class AnnouncementOut(BaseModel):
    id: str
    title: str
    message: str
    category: str
    priority: str
    target_audience: str
    is_active: bool
    created_by: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class NotificationOut(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: str
    sender_id: str
    recipient_id: str
    subject: str
    body: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True


class AnnouncementIn(BaseModel):
    title: str
    message: str
    category: str = "general"
    priority: str = "normal"
    target_audience: str = "all"
    is_active: bool = True


class MessageIn(BaseModel):
    recipient_id: str
    subject: str
    body: str


class NotificationIn(BaseModel):
    user_id: str
    title: str
    message: str
    notification_type: str = "info"


# === ANNOUNCEMENTS ===

@router.get("/announcements", response=List[AnnouncementOut])
def list_announcements(request, category: Optional[str] = Query(None), active_only: bool = Query(True)):
    from messaging.models import Announcement
    queryset = Announcement.objects.all()
    if active_only:
        queryset = queryset.filter(is_active=True)
    if category:
        queryset = queryset.filter(category=category)
    return [
        {
            "id": str(a.id),
            "title": a.title,
            "message": a.message,
            "category": a.category,
            "priority": a.priority,
            "target_audience": a.target_audience,
            "is_active": a.is_active,
            "created_by": str(a.created_by_id) if a.created_by else None,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in queryset
    ]


@router.get("/announcements/{announcement_id}", response=AnnouncementOut)
def get_announcement(request, announcement_id: str):
    from messaging.models import Announcement
    a = Announcement.objects.get(id=announcement_id)
    return {
        "id": str(a.id),
        "title": a.title,
        "message": a.message,
        "category": a.category,
        "priority": a.priority,
        "target_audience": a.target_audience,
        "is_active": a.is_active,
        "created_by": str(a.created_by_id) if a.created_by else None,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.post("/announcements", response=AnnouncementOut)
def create_announcement(request, data: AnnouncementIn):
    from messaging.models import Announcement
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    announcement = Announcement.objects.create(
        title=data.title,
        message=data.message,
        category=data.category,
        priority=data.priority,
        target_audience=data.target_audience,
        is_active=data.is_active,
        created_by=user,
    )
    return {
        "id": str(announcement.id),
        "title": announcement.title,
        "message": announcement.message,
        "category": announcement.category,
        "priority": announcement.priority,
        "target_audience": announcement.target_audience,
        "is_active": announcement.is_active,
        "created_by": str(announcement.created_by_id) if announcement.created_by else None,
        "created_at": announcement.created_at.isoformat() if announcement.created_at else None,
    }


@router.post("/announcements/{announcement_id}")
def toggle_announcement(request, announcement_id: str):
    from messaging.models import Announcement
    a = Announcement.objects.get(id=announcement_id)
    a.is_active = not a.is_active
    a.save()
    return {"status": "success", "id": str(a.id), "is_active": a.is_active}


# === NOTIFICATIONS ===

@router.get("/notifications", response=List[NotificationOut])
def list_notifications(request, user_id: Optional[str] = Query(None), unread_only: bool = Query(False)):
    from messaging.models import Notification
    if user_id:
        queryset = Notification.objects.filter(user_id=user_id)
    else:
        queryset = Notification.objects.all()
    if unread_only:
        queryset = queryset.filter(is_read=False)
    return [
        {
            "id": str(n.id),
            "user_id": str(n.user_id),
            "title": n.title,
            "message": n.message,
            "notification_type": n.notification_type,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in queryset
    ]


@router.post("/notifications/{notification_id}/read")
def mark_notification_read(request, notification_id: str):
    from messaging.models import Notification
    n = Notification.objects.get(id=notification_id)
    n.is_read = True
    n.save()
    return {"status": "success", "id": str(n.id), "is_read": n.is_read}


@router.post("/notifications/mark-all-read")
def mark_all_notifications_read(request, user_id: str):
    from messaging.models import Notification
    updated = Notification.objects.filter(user_id=user_id, is_read=False).update(is_read=True)
    return {"status": "success", "updated_count": updated}


@router.post("/notifications", response=NotificationOut)
def create_notification(request, data: NotificationIn):
    from messaging.models import Notification
    notification = Notification.objects.create(
        user_id=data.user_id,
        title=data.title,
        message=data.message,
        notification_type=data.notification_type,
        is_read=False,
    )
    return {
        "id": str(notification.id),
        "user_id": str(notification.user_id),
        "title": notification.title,
        "message": notification.message,
        "notification_type": notification.notification_type,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat() if notification.created_at else None,
    }


# === MESSAGES ===

@router.get("/messages", response=List[MessageOut])
def list_messages(request, user_id: Optional[str] = Query(None), folder: str = Query("inbox")):
    from messaging.models import Message
    if folder == "sent":
        queryset = Message.objects.filter(sender_id=user_id)
    else:
        queryset = Message.objects.filter(recipient_id=user_id)
    return [
        {
            "id": str(m.id),
            "sender_id": str(m.sender_id),
            "recipient_id": str(m.recipient_id),
            "subject": m.subject,
            "body": m.body,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in queryset
    ]


@router.post("/messages", response=MessageOut)
def send_message(request, data: MessageIn):
    from messaging.models import Message
    from django.contrib.auth import get_user_model
    User = get_user_model()
    sender = User.objects.first()
    message = Message.objects.create(
        sender_id=str(sender.id) if sender else "system",
        recipient_id=data.recipient_id,
        subject=data.subject,
        body=data.body,
        is_read=False,
    )
    return {
        "id": str(message.id),
        "sender_id": message.sender_id,
        "recipient_id": message.recipient_id,
        "subject": message.subject,
        "body": message.body,
        "is_read": message.is_read,
        "created_at": message.created_at.isoformat() if message.created_at else None,
    }


# === STATS ===

@router.get("/stats")
def messaging_stats(request, user_id: Optional[str] = Query(None)):
    from messaging.models import Announcement, Notification, Message
    announcements = Announcement.objects.filter(is_active=True).count()
    notifications_unread = Notification.objects.filter(is_read=False).count()
    messages_unread = Message.objects.filter(recipient_id=user_id, is_read=False).count() if user_id else 0
    return {
        "active_announcements": announcements,
        "unread_notifications": notifications_unread,
        "unread_messages": messages_unread,
    }