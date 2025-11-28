from django import forms
from .models import Person
import re


class PersonAdminForm(forms.ModelForm):
    """Simplified form for admin registration."""
    
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'notification_preference', 'is_active', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.HiddenInput(),  # Hidden, populated by JavaScript international input
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notification_preference': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        if not phone_number:
            raise forms.ValidationError('Phone number is required.')
        
        # Ensure it's in E.164 format (starts with +)
        if not phone_number.startswith('+'):
            # Try to clean and add +
            cleaned = re.sub(r'[^\d+]', '', phone_number)
            if cleaned:
                phone_number = '+' + cleaned.lstrip('+')
            else:
                raise forms.ValidationError('Please enter a valid phone number.')
        
        # Validate length
        if len(phone_number) > 20:
            raise forms.ValidationError('Phone number is too long.')
        
        if len(phone_number) < 8:
            raise forms.ValidationError('Phone number is too short.')
        
        # Check for duplicates (exclude current instance if editing)
        existing = Person.objects.filter(phone_number=phone_number)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError('This phone number is already registered.')
        
        return phone_number


class PersonRegistrationForm(forms.ModelForm):
    """Form for public registration."""
    
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'notification_preference']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone_number': forms.HiddenInput(),  # Hidden, populated by JavaScript
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}),
            'notification_preference': forms.HiddenInput(),  # We'll handle it with custom radio buttons
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        if not phone_number:
            raise forms.ValidationError('Phone number is required.')
        
        # Ensure it's in E.164 format (starts with +)
        if not phone_number.startswith('+'):
            # Try to clean and add +
            cleaned = re.sub(r'[^\d+]', '', phone_number)
            if cleaned:
                phone_number = '+' + cleaned.lstrip('+')
            else:
                raise forms.ValidationError('Please enter a valid phone number.')
        
        # Validate length (E.164 format: max 15 characters including +)
        if len(phone_number) > 20:
            raise forms.ValidationError('Phone number is too long.')
        
        if len(phone_number) < 8:  # Minimum reasonable length
            raise forms.ValidationError('Phone number is too short.')
        
        if Person.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('This phone number is already registered.')
        
        return phone_number
    
    def clean_notification_preference(self):
        preference = self.cleaned_data.get('notification_preference')
        # Get from POST data if not in cleaned_data (since we use custom radio buttons)
        if not preference:
            preference = self.data.get('notification_preference', 'whatsapp')
        return preference or 'whatsapp'  # Default to whatsapp if not provided

