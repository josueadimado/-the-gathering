from django import forms
from .models import Attendance
from people.models import Person
from events.models import Event


class CheckInForm(forms.ModelForm):
    """Form for manual check-in."""
    
    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a person..."
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select an event..."
    )
    
    class Meta:
        model = Attendance
        fields = ['person', 'event', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        person = cleaned_data.get('person')
        event = cleaned_data.get('event')
        
        if person and event:
            # Check if already checked in
            if Attendance.objects.filter(person=person, event=event).exists():
                raise forms.ValidationError(
                    f'{person.get_full_name()} is already checked in for this event.'
                )
        
        return cleaned_data

