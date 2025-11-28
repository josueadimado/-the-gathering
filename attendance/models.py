from django.db import models
from django.utils import timezone
from people.models import Person
from events.models import Event


class Attendance(models.Model):
    """Model to track attendance records."""
    
    CHECK_IN_METHOD_CHOICES = [
        ('qr', 'QR Code'),
        ('manual', 'Manual Search'),
        ('admin', 'Admin Entry'),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    check_in_time = models.DateTimeField(default=timezone.now)
    check_in_method = models.CharField(max_length=20, choices=CHECK_IN_METHOD_CHOICES, default='manual')
    checked_in_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_in_records'
    )
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-check_in_time']
        unique_together = ['person', 'event']  # Prevent duplicate check-ins
    
    def __str__(self):
        return f"{self.person.get_full_name()} - {self.event.name}"

