from django.db import models
from django.utils import timezone


class Event(models.Model):
    """Model to store information about events/gatherings."""
    
    EVENT_TYPE_CHOICES = [
        ('weekly', 'Weekly Gathering'),
        ('special', 'Special Event'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=200, blank=True, null=True, help_text='Topic or theme for this event')
    event_date = models.DateField()
    event_time = models.TimeField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='weekly')
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True, help_text='Upload an image for this event')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date', '-event_time']
    
    def __str__(self):
        return f"{self.name} - {self.event_date}"
    
    def is_upcoming(self):
        """Check if event is in the future."""
        from django.utils import timezone
        event_datetime = timezone.make_aware(
            timezone.datetime.combine(self.event_date, self.event_time)
        )
        return event_datetime > timezone.now()

