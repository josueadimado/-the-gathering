from django import forms
from .models import MessageTemplate
from people.models import Person
from events.models import Event


class MessageTemplateForm(forms.ModelForm):
    """Form for creating/editing message templates."""
    
    class Meta:
        model = MessageTemplate
        fields = ['name', 'message_type', 'subject', 'body', 'variables', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'message_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'variables': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'body': 'Use variables like {name}, {event_name}, {event_date}, {event_time}, {event_location}',
            'variables': 'Comma-separated list of available variables',
        }


class SendMessageForm(forms.Form):
    """Form for sending messages to people."""
    
    template = forms.ModelChoiceField(
        queryset=MessageTemplate.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a template..."
    )
    
    people = forms.ModelMultipleChoiceField(
        queryset=Person.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10'}),
        required=True,
        help_text="Hold Ctrl (Cmd on Mac) to select multiple people"
    )
    
    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label="No event (optional)"
    )
