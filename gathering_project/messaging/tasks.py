"""
Celery tasks for scheduled messaging.
Will be implemented when Celery is set up.
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from events.models import Event
from people.models import Person
from messaging.models import MessageTemplate
from messaging.services import send_message


@shared_task
def send_event_reminders():
    """
    Send reminders for upcoming events.
    This task should run daily to check for events happening in the next 24 hours.
    """
    # Find events happening tomorrow
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_events = Event.objects.filter(
        event_date=tomorrow,
        is_active=True
    )
    
    # Get reminder template (you'll need to create this)
    try:
        template = MessageTemplate.objects.get(name='Event Reminder', is_active=True)
    except MessageTemplate.DoesNotExist:
        return "No reminder template found"
    
    # Send reminders to all active people
    people = Person.objects.filter(is_active=True)
    sent_count = 0
    
    for event in upcoming_events:
        for person in people:
            if person.phone_number:  # Only send if they have a phone number
                try:
                    send_message(person, template, event)
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending message to {person.get_full_name()}: {e}")
    
    return f"Sent {sent_count} reminders for {upcoming_events.count()} events"

