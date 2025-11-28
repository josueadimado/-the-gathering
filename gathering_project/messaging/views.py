from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import MessageTemplate, MessageLog
from .forms import MessageTemplateForm, SendMessageForm
from .services import send_message
from .utils import update_message_statuses
from people.models import Person
from events.models import Event

# Create your views here.

@login_required
def template_list(request):
    """List all message templates."""
    templates = MessageTemplate.objects.all()
    context = {
        'templates': templates,
    }
    return render(request, 'messaging/template_list.html', context)


@login_required
def template_create(request):
    """Create a new message template."""
    if request.method == 'POST':
        form = MessageTemplateForm(request.POST)
        if form.is_valid():
            template = form.save()
            messages.success(request, f'Template "{template.name}" created successfully!')
            return redirect('messaging:template_detail', pk=template.pk)
    else:
        form = MessageTemplateForm()
    
    return render(request, 'messaging/template_form.html', {'form': form, 'action': 'Create'})


@login_required
def template_detail(request, pk):
    """View details of a message template."""
    template = get_object_or_404(MessageTemplate, pk=pk)
    return render(request, 'messaging/template_detail.html', {'template': template})


@login_required
def template_update(request, pk):
    """Update an existing message template."""
    template = get_object_or_404(MessageTemplate, pk=pk)
    
    if request.method == 'POST':
        form = MessageTemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save()
            messages.success(request, f'Template "{template.name}" updated successfully!')
            return redirect('messaging:template_detail', pk=template.pk)
    else:
        form = MessageTemplateForm(instance=template)
    
    return render(request, 'messaging/template_form.html', {'form': form, 'action': 'Update', 'template': template})


@login_required
def message_log_list(request):
    """List all sent messages with summary statistics."""
    # Optional: refresh delivery statuses from API when ?refresh=1 is present
    # Limited to recent messages (last 24 hours, max 50) for performance
    if request.GET.get("refresh") == "1":
        updated_count, total_checked = update_message_statuses(limit=50, hours=24)
        if updated_count > 0:
            messages.success(request, f"Updated delivery status for {updated_count} of {total_checked} recent message(s).")
        else:
            messages.info(request, f"Checked {total_checked} recent message(s). No status updates needed.")

    message_logs = MessageLog.objects.all()
    
    # Filter by status and type
    filter_status = request.GET.get('status', 'all')
    filter_type = request.GET.get('type', 'all')
    
    if filter_status != 'all':
        message_logs = message_logs.filter(status=filter_status)
    
    if filter_type != 'all':
        message_logs = message_logs.filter(message_type=filter_type)
    
    # Get summary statistics (from all messages, not filtered)
    all_logs = MessageLog.objects.all()
    total_count = all_logs.count()
    sent_count = all_logs.filter(status='sent').count()
    failed_count = all_logs.filter(status='failed').count()
    pending_count = all_logs.filter(status='pending').count()
    delivered_count = all_logs.filter(status='delivered').count()
    
    # Recent batch statistics (last hour)
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_logs = all_logs.filter(created_at__gte=one_hour_ago)
    recent_total = recent_logs.count()
    recent_sent = recent_logs.filter(status='sent').count()
    recent_failed = recent_logs.filter(status='failed').count()
    recent_pending = recent_logs.filter(status='pending').count()
    
    # Pagination
    paginator = Paginator(message_logs.order_by('-created_at'), 50)  # 50 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'message_logs': page_obj,
        'page_obj': page_obj,
        'filter_status': filter_status,
        'filter_type': filter_type,
        # Summary statistics
        'total_count': total_count,
        'sent_count': sent_count,
        'failed_count': failed_count,
        'pending_count': pending_count,
        'delivered_count': delivered_count,
        # Recent batch (last hour)
        'recent_total': recent_total,
        'recent_sent': recent_sent,
        'recent_failed': recent_failed,
        'recent_pending': recent_pending,
    }
    return render(request, 'messaging/message_log_list.html', context)


@login_required
def send_test_message(request, template_id):
    """Send a test message using a template."""
    template = get_object_or_404(MessageTemplate, pk=template_id)
    # Implementation will be added when messaging service is integrated
    messages.info(request, 'Test message functionality will be available after API integration.')
    return redirect('messaging:template_detail', pk=template.pk)


@login_required
def send_message_view(request, pk):
    """Send messages to selected people using a template."""
    template = get_object_or_404(MessageTemplate, pk=pk)
    
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        form.fields['template'].queryset = MessageTemplate.objects.filter(pk=template.pk)
        form.fields['template'].initial = template
        
        if form.is_valid():
            selected_people = form.cleaned_data['people']
            selected_event = form.cleaned_data.get('event')
            
            success_count = 0
            error_count = 0
            
            for person in selected_people:
                try:
                    # Check if person has the required contact info
                    if template.message_type in ['sms', 'whatsapp']:
                        if not person.phone_number:
                            error_count += 1
                            continue
                    elif template.message_type == 'email':
                        if not person.email:
                            error_count += 1
                            continue
                    
                    # Send the message
                    message_log = send_message(person, template, selected_event)
                    if message_log.status == 'sent':
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    # Log the error but continue with other people
            
            if success_count > 0:
                messages.success(request, f'Successfully sent {success_count} message(s)!')
            if error_count > 0:
                messages.warning(request, f'{error_count} message(s) failed to send.')
            
            return redirect('messaging:message_log_list')
    else:
        form = SendMessageForm(initial={'template': template})
        form.fields['template'].queryset = MessageTemplate.objects.filter(pk=template.pk)
    
    # Get people count for display
    total_people = Person.objects.filter(is_active=True).count()
    
    context = {
        'form': form,
        'template': template,
        'total_people': total_people,
    }
    return render(request, 'messaging/send_message.html', context)

