from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Attendance
from .forms import CheckInForm
from people.models import Person
from events.models import Event

# Create your views here.

def self_check_in(request):
    """Public self-service check-in page - no login required."""
    error_message = None
    success_message = None
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(
        is_active=True,
        event_date__gte=timezone.now().date()
    ).order_by('event_date', 'event_time')[:5]
    
    # Find the next upcoming Saturday event
    today = timezone.now().date()
    days_until_saturday = (5 - today.weekday()) % 7  # Saturday is weekday 5
    
    # If today is Saturday, check today first, otherwise get next Saturday
    if days_until_saturday == 0:  # Today is Saturday
        next_saturday = today
    else:
        next_saturday = today + timedelta(days=days_until_saturday)
    
    # Try to find an event on the next Saturday
    default_event = None
    saturday_events = Event.objects.filter(
        is_active=True,
        event_date=next_saturday
    ).order_by('event_time').first()
    
    if saturday_events:
        default_event = saturday_events
    elif upcoming_events.exists():
        # If no Saturday event found, use the first upcoming event
        default_event = upcoming_events.first()
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        event_id = request.POST.get('event_id')
        
        if not phone_number:
            error_message = "Please enter your phone number."
        elif not event_id:
            error_message = "Please select an event."
        else:
            try:
                # Find person by phone number
                person = Person.objects.get(phone_number=phone_number, is_active=True)
                event = Event.objects.get(pk=event_id, is_active=True)
                
                # Check if already checked in
                if Attendance.objects.filter(person=person, event=event).exists():
                    error_message = f"You are already checked in for {event.name}."
                else:
                    # Create attendance record
                    Attendance.objects.create(
                        person=person,
                        event=event,
                        check_in_method='manual',
                        checked_in_by=None  # Self check-in
                    )
                    success_message = f"Successfully checked in for {event.name}! Welcome, {person.get_full_name()}."
                    
            except Person.DoesNotExist:
                error_message = "Phone number not found. Please register first or contact administrator."
            except Event.DoesNotExist:
                error_message = "Invalid event selected."
            except Exception as e:
                error_message = "An error occurred. Please try again or contact administrator."
    
    context = {
        'upcoming_events': upcoming_events,
        'default_event_id': default_event.pk if default_event else None,
        'error_message': error_message,
        'success_message': success_message,
    }
    return render(request, 'attendance/self_check_in.html', context)


@login_required
def check_in(request):
    """Main check-in interface with QR scanner and manual search."""
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.checked_in_by = request.user
            attendance.save()
            messages.success(request, f'{attendance.person.get_full_name()} checked in successfully!')
            return redirect('attendance:check_in')
    else:
        form = CheckInForm()
    
    # Get upcoming events for the form
    upcoming_events = Event.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'attendance/check_in.html', context)


@login_required
def check_in_qr(request):
    """Handle QR code check-in via AJAX."""
    if request.method == 'POST':
        person_id = request.POST.get('person_id', '').strip()
        event_id = request.POST.get('event_id', '').strip()
        
        if not person_id or not event_id:
            return JsonResponse({
                'success': False,
                'message': 'Person ID and Event ID are required.'
            })
        
        try:
            # Try to get person by ID (UUID) or by qr_code field
            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                # Try finding by qr_code field as fallback
                person = Person.objects.get(qr_code=person_id)
            
            event = Event.objects.get(pk=event_id)
            
            # Check if person is active
            if not person.is_active:
                return JsonResponse({
                    'success': False,
                    'message': f'{person.get_full_name()} is not active.'
                })
            
            # Check if already checked in
            if Attendance.objects.filter(person=person, event=event).exists():
                return JsonResponse({
                    'success': False,
                    'message': f'{person.get_full_name()} is already checked in for this event.'
                })
            
            # Create attendance record
            attendance = Attendance.objects.create(
                person=person,
                event=event,
                check_in_method='qr',
                checked_in_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': f'{person.get_full_name()} checked in successfully!'
            })
        except Person.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Person not found. Please ensure the QR code is valid.'
            })
        except Event.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Event not found.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def search_person(request):
    """Search for a person by name or phone (for manual check-in)."""
    query = request.GET.get('q', '')
    if query:
        people = Person.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query)
        )[:10]  # Limit to 10 results
        results = [{'id': str(p.id), 'name': p.get_full_name(), 'phone': p.phone_number} for p in people]
    else:
        results = []
    
    return JsonResponse({'results': results})


@login_required
def attendance_list(request, event_id=None):
    """List attendance records, optionally filtered by event."""
    attendances = Attendance.objects.all()
    
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
        attendances = attendances.filter(event=event)
    else:
        event = None
    
    context = {
        'attendances': attendances,
        'event': event,
    }
    return render(request, 'attendance/attendance_list.html', context)


@login_required
def person_attendance_history(request, person_id):
    """View attendance history for a specific person."""
    person = get_object_or_404(Person, pk=person_id)
    attendances = Attendance.objects.filter(person=person)
    
    context = {
        'person': person,
        'attendances': attendances,
    }
    return render(request, 'attendance/person_history.html', context)
