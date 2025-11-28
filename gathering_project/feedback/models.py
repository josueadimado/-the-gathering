from django.db import models
from django.utils import timezone
from people.models import Person


class Feedback(models.Model):
    """Model to store feedback, suggestions, and prayer requests."""
    
    FEEDBACK_TYPE_CHOICES = [
        ('suggestion', 'Suggestion'),
        ('prayer_request', 'Prayer Request'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('addressed', 'Addressed'),
        ('closed', 'Closed'),
    ]
    
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks'
    )
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='other')
    message = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_feedbacks'
    )
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        if self.is_anonymous:
            return f"Anonymous {self.get_feedback_type_display()} - {self.submitted_at.strftime('%Y-%m-%d')}"
        elif self.person:
            return f"{self.person.get_full_name()} - {self.get_feedback_type_display()}"
        else:
            return f"{self.get_feedback_type_display()} - {self.submitted_at.strftime('%Y-%m-%d')}"

