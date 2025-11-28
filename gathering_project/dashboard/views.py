from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from people.models import Person
from events.models import Event
from attendance.models import Attendance
from feedback.models import Feedback

# Create your views here.

@login_required
def index(request):
    """Main dashboard with key metrics."""
    
    # Total registered people
    total_people = Person.objects.filter(is_active=True).count()
    
    # Total events
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(is_active=True)
    
    # Recent registrations (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_registrations = Person.objects.filter(date_registered__gte=thirty_days_ago).count()
    
    # Total attendance records
    total_attendance = Attendance.objects.count()
    
    # Recent attendance (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_attendance = Attendance.objects.filter(check_in_time__gte=seven_days_ago).count()
    
    # Pending feedback
    pending_feedback = Feedback.objects.filter(status='new').count()
    
    # Upcoming events (next 7 days)
    next_week = timezone.now().date() + timedelta(days=7)
    upcoming_events_list = Event.objects.filter(
        event_date__lte=next_week,
        event_date__gte=timezone.now().date(),
        is_active=True
    ).order_by('event_date', 'event_time')[:5]
    
    # Most recent registrations
    recent_people = Person.objects.filter(is_active=True).order_by('-date_registered')[:5]
    
    context = {
        'total_people': total_people,
        'total_events': total_events,
        'recent_registrations': recent_registrations,
        'total_attendance': total_attendance,
        'recent_attendance': recent_attendance,
        'pending_feedback': pending_feedback,
        'upcoming_events': upcoming_events_list,
        'recent_people': recent_people,
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def attendance_analytics(request):
    """Detailed attendance analytics."""
    
    # Total attendance
    total_attendance = Attendance.objects.count()
    
    # Attendance by event (top 10)
    event_attendance = Event.objects.annotate(
        attendance_count=Count('attendances')
    ).filter(attendance_count__gt=0).order_by('-attendance_count')[:10]
    
    # Attendance trends (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_attendances = Attendance.objects.filter(check_in_time__gte=thirty_days_ago)
    recent_count = recent_attendances.count()
    
    # Attendance by check-in method
    check_in_methods = Attendance.objects.values('check_in_method').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Attendance by day (last 30 days) - simplified
    attendance_by_day = recent_attendances.extra(
        select={'day': "date(check_in_time)"}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    # Average attendance per event
    events_with_attendance = Event.objects.annotate(
        attendance_count=Count('attendances')
    ).filter(attendance_count__gt=0)
    if events_with_attendance.count() > 0:
        avg_attendance = sum(e.attendance_count for e in events_with_attendance) / events_with_attendance.count()
    else:
        avg_attendance = 0
    
    # Most recent check-ins
    recent_checkins = Attendance.objects.select_related('person', 'event').order_by('-check_in_time')[:10]
    
    context = {
        'total_attendance': total_attendance,
        'recent_count': recent_count,
        'event_attendance': event_attendance,
        'recent_attendances': recent_attendances,
        'check_in_methods': check_in_methods,
        'attendance_by_day': attendance_by_day,
        'avg_attendance': round(avg_attendance, 1),
        'recent_checkins': recent_checkins,
    }
    
    return render(request, 'dashboard/attendance_analytics.html', context)


@login_required
def people_analytics(request):
    """People registration analytics."""
    
    # Total people
    total_people = Person.objects.filter(is_active=True).count()
    inactive_people = Person.objects.filter(is_active=False).count()
    
    # Registration trends (last 12 months)
    twelve_months_ago = timezone.now() - timedelta(days=365)
    registrations_by_month = Person.objects.filter(
        date_registered__gte=twelve_months_ago
    ).extra(
        select={'month': "strftime('%%Y-%%m', date_registered)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Recent registrations (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_registrations = Person.objects.filter(date_registered__gte=thirty_days_ago).count()
    
    # Most active attendees (by attendance count)
    active_attendees = Person.objects.annotate(
        attendance_count=Count('attendances')
    ).filter(attendance_count__gt=0, is_active=True).order_by('-attendance_count')[:10]
    
    # People by notification preference
    notification_prefs = Person.objects.values('notification_preference').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # People who have never attended
    people_with_attendance = Person.objects.filter(attendances__isnull=False).distinct().count()
    people_without_attendance = total_people - people_with_attendance
    
    # Registration by month (last 6 months for better visualization)
    six_months_ago = timezone.now() - timedelta(days=180)
    recent_registrations_by_month = Person.objects.filter(
        date_registered__gte=six_months_ago
    ).extra(
        select={'month': "strftime('%%Y-%%m', date_registered)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_people': total_people,
        'inactive_people': inactive_people,
        'registrations_by_month': registrations_by_month,
        'recent_registrations_by_month': recent_registrations_by_month,
        'recent_registrations': recent_registrations,
        'active_attendees': active_attendees,
        'notification_prefs': notification_prefs,
        'people_with_attendance': people_with_attendance,
        'people_without_attendance': people_without_attendance,
    }
    
    return render(request, 'dashboard/people_analytics.html', context)

