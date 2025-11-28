from django import forms
from .models import Feedback
from people.models import Person


class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback."""
    
    # Optional: Allow selecting person if they're registered
    person_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'}),
        help_text='If you\'re registered, enter your phone number to link this feedback to your account.'
    )
    
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'message', 'is_anonymous']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Enter your feedback, suggestion, or prayer request...'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        person_phone = cleaned_data.get('person_phone')
        is_anonymous = cleaned_data.get('is_anonymous')
        
        # Try to find person by phone if provided
        if person_phone and not is_anonymous:
            try:
                person = Person.objects.get(phone_number=person_phone)
                cleaned_data['person'] = person
            except Person.DoesNotExist:
                # Person not found, that's okay - feedback can be submitted without linking
                pass
        
        return cleaned_data

