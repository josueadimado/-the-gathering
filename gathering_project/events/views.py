from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
import qrcode
import io
from .models import Event
from .forms import EventForm

# Create your views here.

@login_required
def event_list(request):
    """List all events."""
    events = Event.objects.all()
    
    # Filter by status if requested
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'upcoming':
        events = [e for e in events if e.is_upcoming()]
    elif filter_type == 'past':
        events = [e for e in events if not e.is_upcoming()]
    
    context = {
        'events': events,
        'filter_type': filter_type,
    }
    return render(request, 'events/event_list.html', context)


@login_required
def event_create(request):
    """Create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})


@login_required
def event_detail(request, pk):
    """View details of a specific event."""
    event = get_object_or_404(Event, pk=pk)
    # Get attendance for this event
    from attendance.models import Attendance
    attendance_list = Attendance.objects.filter(event=event)
    
    context = {
        'event': event,
        'attendance_list': attendance_list,
        'attendance_count': attendance_list.count(),
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_update(request, pk):
    """Update an existing event."""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Update', 'event': event})


@login_required
def event_delete(request, pk):
    """Delete an event."""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Event "{event_name}" deleted successfully!')
        return redirect('events:list')
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})


def event_qr_code(request, pk):
    """Generate and return QR code image for an event (public access)."""
    try:
        event = get_object_or_404(Event, pk=pk)
        
        # Import here to avoid issues if Pillow is not installed
        try:
            from PIL import Image
        except ImportError:
            return HttpResponse("Pillow is not installed. Please install it: pip install Pillow", 
                              content_type='text/plain', status=500)
        
        # Create QR code with event check-in URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # QR code data contains the event self-check-in URL (public access)
        from django.urls import reverse
        try:
            # Use self_check_in which is public (no login required)
            self_check_in_url = reverse('attendance:self_check_in')
            qr_data = request.build_absolute_uri(self_check_in_url + f'?event={event.pk}')
        except Exception as url_error:
            # If URL reverse fails, construct the URL manually
            base_url = request.build_absolute_uri('/')
            qr_data = f"{base_url}attendance/self-check-in/?event={event.pk}"
        
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        image_data = buffer.getvalue()
        buffer.close()
        
        # Return as HTTP response with proper headers
        response = HttpResponse(image_data, content_type='image/png')
        response['Content-Disposition'] = f'inline; filename="event_{event.pk}_qr.png"'
        response['Cache-Control'] = 'public, max-age=3600'
        return response
        
    except Exception as e:
        # Log the error and return a proper error response
        import traceback
        error_msg = f"Error generating QR code: {str(e)}\n{traceback.format_exc()}"
        return HttpResponse(error_msg, content_type='text/plain', status=500)


def event_qr_scan(request, pk):
    """Public page to display QR code for scanning to log attendance."""
    event = get_object_or_404(Event, pk=pk)
    
    context = {
        'event': event,
    }
    return render(request, 'events/qr_scan.html', context)

