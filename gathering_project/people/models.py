from django.db import models
from django.utils import timezone
import uuid


class Person(models.Model):
    """Model to store information about registered attendees."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True, help_text="International format: +1234567890")
    email = models.EmailField(blank=True, null=True)
    notification_preference = models.CharField(
        max_length=20,
        choices=[
            ('whatsapp', 'WhatsApp'),
            ('sms', 'SMS'),
            ('both', 'Both'),
            ('none', 'None'),
        ],
        default='whatsapp',
        help_text="Preferred method for event reminders and notifications"
    )
    date_registered = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    qr_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_registered']
        verbose_name_plural = 'People'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        # Generate QR code if not already set
        if not self.qr_code:
            # Use the person's UUID as the QR code value
            self.qr_code = str(self.id)
        super().save(*args, **kwargs)

