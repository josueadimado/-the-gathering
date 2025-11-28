from django.shortcuts import render
from django.utils import timezone
from events.models import Event


def landing(request):
    """Public landing page with upcoming events."""
    # Get upcoming events (active events from today onwards)
    upcoming_events = Event.objects.filter(
        is_active=True,
        event_date__gte=timezone.now().date()
    ).order_by('event_date', 'event_time')[:5]  # Limit to 5 upcoming events
    
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request, 'landing.html', context)

