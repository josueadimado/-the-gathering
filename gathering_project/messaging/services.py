"""
Messaging service - Handles sending messages via SMS/WhatsApp/Email.
"""
from django.conf import settings
from django.utils import timezone
from .models import MessageLog
from .api_client import SMSAPIClient
import logging

logger = logging.getLogger(__name__)


def send_message(person, template, event=None):
    """
    Send a message to a person using a template.
    
    Args:
        person: Person instance
        template: MessageTemplate instance
        event: Event instance (optional)
    
    Returns:
        MessageLog instance
    """
    # Format message body with variables
    body = template.body
    if event:
        body = body.replace('{event_name}', event.name or '')
        body = body.replace('{event_date}', str(event.event_date) if event.event_date else '')
        body = body.replace('{event_time}', str(event.event_time) if event.event_time else '')
        body = body.replace('{event_location}', event.location or '')
        body = body.replace('{event_topic}', event.topic or '')
    
    body = body.replace('{name}', person.get_full_name())
    
    # Determine recipient
    if template.message_type == 'email':
        recipient = person.email or ''
    else:
        recipient = person.phone_number
    
    # Create message log
    message_log = MessageLog.objects.create(
        person=person,
        event=event,
        template=template,
        message_type=template.message_type,
        recipient=recipient,
        subject=template.subject,
        body=body,
        status='pending'
    )
    
    # Send the message based on type
    try:
        if template.message_type in ['sms', 'whatsapp']:
            result = send_sms_or_whatsapp(recipient, body, template.message_type)
            if result['success']:
                message_log.status = 'sent'
                message_log.sent_at = timezone.now()
                # Store message ID if available
                if 'message_id' in result:
                    message_log.external_id = result['message_id']
            else:
                message_log.status = 'failed'
                message_log.error_message = result.get('error', 'Unknown error')
        elif template.message_type == 'email':
            result = send_email(recipient, template.subject or '', body)
            if result['success']:
                message_log.status = 'sent'
                message_log.sent_at = timezone.now()
            else:
                message_log.status = 'failed'
                message_log.error_message = result.get('error', 'Unknown error')
        
        message_log.save()
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        message_log.status = 'failed'
        message_log.error_message = str(e)
        message_log.save()
    
    return message_log


def send_sms_or_whatsapp(phone_number, message_body, message_type='sms'):
    """
    Send SMS or WhatsApp message using the SMS API.
    
    Args:
        phone_number: Recipient phone number (E.164 format)
        message_body: Message text
        message_type: 'sms' or 'whatsapp'
    
    Returns:
        dict with 'success' (bool), 'message_id' (str), 'cost' (float),
        'currency' (str), 'segments' (int), and optional 'error' (str)
    """
    # Use SMS API for sending messages
    api_client = SMSAPIClient()
    
    # For WhatsApp, we still use SMS API but may need special handling
    # Check if API is configured
    if not getattr(settings, 'SMS_API_PUBLIC_KEY', '') or not getattr(settings, 'SMS_API_SECRET_KEY', ''):
        # Fallback to Twilio if API not configured (for backward compatibility)
        return _send_via_twilio(phone_number, message_body, message_type)
    
    # Send via SMS API
    result = api_client.send_sms(
        to=phone_number,
        body=message_body,
        sender_id=getattr(settings, 'SMS_SENDER_ID', 'TheGathering')
    )
    
    return result


def _send_via_twilio(phone_number, message_body, message_type='sms'):
    """
    Fallback method to send via Twilio (for backward compatibility).
    """
    try:
        from twilio.rest import Client
        
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_number = settings.TWILIO_PHONE_NUMBER
        
        # Check if Twilio is configured
        if not account_sid or not auth_token or not from_number:
            return {
                'success': False,
                'error': 'SMS service not configured. Please add SMS_API_KEY or Twilio credentials to your .env file.'
            }
        
        client = Client(account_sid, auth_token)
        
        # Determine the "from" number format based on message type
        if message_type == 'whatsapp':
            # WhatsApp format: whatsapp:+1234567890
            from_whatsapp = f"whatsapp:{from_number}"
            to_whatsapp = f"whatsapp:{phone_number}"
            
            message = client.messages.create(
                body=message_body,
                from_=from_whatsapp,
                to=to_whatsapp
            )
        else:
            # Regular SMS
            message = client.messages.create(
                body=message_body,
                from_=from_number,
                to=phone_number
            )
        
        return {
            'success': True,
            'message_id': message.sid,
            'cost': 0,  # Twilio doesn't return cost in this response
            'currency': 'USD',
            'segments': 1,
        }
        
    except ImportError:
        return {
            'success': False,
            'error': 'SMS service not available. Please configure SMS_API_KEY in your .env file.'
        }
    except Exception as e:
        logger.error(f"Twilio error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def send_email(recipient_email, subject, message_body):
    """
    Send email message.
    
    Args:
        recipient_email: Recipient email address
        subject: Email subject
        message_body: Email body
    
    Returns:
        dict with 'success' (bool) and optional 'error' (str)
    """
    try:
        from django.core.mail import send_mail
        
        send_mail(
            subject=subject or 'Message from The Gathering',
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        return {'success': True}
        
    except Exception as e:
        logger.error(f"Email error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

