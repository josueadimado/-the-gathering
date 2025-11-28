from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm

# Create your views here.

def submit_feedback(request):
    """Public feedback submission form - no login required."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            messages.success(request, 'Thank you for your feedback! We appreciate your input.')
            return redirect('feedback:submit_success')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit.html', {'form': form})


def submit_success(request):
    """Success page after feedback submission."""
    return render(request, 'feedback/submit_success.html')


@login_required
def feedback_list(request):
    """List all feedback (admin only)."""
    feedback_list = Feedback.objects.all()
    
    # Filter by type and status
    filter_type = request.GET.get('type', 'all')
    filter_status = request.GET.get('status', 'all')
    
    if filter_type != 'all':
        feedback_list = feedback_list.filter(feedback_type=filter_type)
    
    if filter_status != 'all':
        feedback_list = feedback_list.filter(status=filter_status)
    
    context = {
        'feedback_list': feedback_list,
        'filter_type': filter_type,
        'filter_status': filter_status,
    }
    return render(request, 'feedback/feedback_list.html', context)


@login_required
def feedback_detail(request, pk):
    """View details of specific feedback (admin only)."""
    feedback = get_object_or_404(Feedback, pk=pk)
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})


@login_required
def feedback_update_status(request, pk):
    """Update feedback status (admin only)."""
    feedback = get_object_or_404(Feedback, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        
        if new_status in dict(Feedback.STATUS_CHOICES):
            feedback.status = new_status
            feedback.admin_notes = admin_notes
            if new_status != 'new':
                from django.utils import timezone
                feedback.reviewed_at = timezone.now()
                feedback.reviewed_by = request.user
            feedback.save()
            messages.success(request, 'Feedback status updated successfully!')
            return redirect('feedback:detail', pk=feedback.pk)
    
    return redirect('feedback:detail', pk=feedback.pk)

