from django.db import models
from django.utils import timezone
from people.models import Person
from events.models import Event


class MessageTemplate(models.Model):
    """Model to store reusable message templates."""
    
    MESSAGE_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ]
    
    name = models.CharField(max_length=100)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='sms')
    subject = models.CharField(max_length=200, blank=True, null=True)  # For email
    body = models.TextField()
    variables = models.CharField(
        max_length=500,
        blank=True,
        help_text='Available variables: {name}, {event_name}, {event_date}, {event_time}, {event_location}, {event_topic}'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_message_type_display()})"


class MessageLog(models.Model):
    """Model to track sent messages."""
    
    MESSAGE_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='messages')
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )
    template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs'
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    recipient = models.CharField(max_length=100)  # Phone number or email
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    external_id = models.CharField(max_length=200, blank=True, null=True, help_text='External message ID from API')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.person.get_full_name()} - {self.get_status_display()} - {self.created_at}"

