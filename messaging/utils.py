"""
Utility functions for messaging.
"""
from .api_client import SMSAPIClient
from .models import MessageLog
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def check_message_status(message_log):
    """
    Check and update the status of a message log using the API.
    
    Args:
        message_log: MessageLog instance
    
    Returns:
        bool: True if status was updated, False otherwise
    """
    if not message_log.external_id:
        return False
    
    if message_log.message_type not in ['sms', 'whatsapp']:
        return False
    
    try:
        api_client = SMSAPIClient()
        result = api_client.check_message_status(message_log.external_id)
        
        if result['success']:
            new_status = result.get('status', message_log.status)
            
            # Map API status to our status choices
            status_mapping = {
                'pending': 'pending',
                'sent': 'sent',
                'delivered': 'delivered',
                'failed': 'failed',
                'read': 'delivered',  # WhatsApp read status
            }
            
            mapped_status = status_mapping.get(new_status, message_log.status)
            
            if mapped_status != message_log.status:
                message_log.status = mapped_status
                
                # Update delivered_at if available
                if result.get('delivered_at') and mapped_status == 'delivered':
                    try:
                        from datetime import datetime
                        delivered_at = datetime.fromisoformat(result['delivered_at'].replace('Z', '+00:00'))
                        # Note: We don't have a delivered_at field yet, but we can add it if needed
                    except:
                        pass
                
                message_log.save()
                return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error checking message status: {str(e)}")
        return False


def update_message_statuses(limit=50, hours=24):
    """
    Update statuses for recent pending/sent messages that have external IDs.
    Optimized to only check recent messages to avoid slow performance.
    
    Args:
        limit: Maximum number of messages to check (default: 50)
        hours: Only check messages from the last N hours (default: 24)
    
    Returns:
        tuple: (updated_count, total_checked)
    """
    from datetime import timedelta
    
    # Only check recent messages (last 24 hours by default) to keep it fast
    cutoff_time = timezone.now() - timedelta(hours=hours)
    
    message_logs = MessageLog.objects.filter(
        external_id__isnull=False,
        status__in=['pending', 'sent'],
        message_type__in=['sms', 'whatsapp'],
        created_at__gte=cutoff_time  # Only recent messages
    ).order_by('-created_at')[:limit]  # Limit to most recent N messages
    
    updated_count = 0
    total_checked = 0
    
    for message_log in message_logs:
        total_checked += 1
        if check_message_status(message_log):
            updated_count += 1
    
    return updated_count, total_checked

