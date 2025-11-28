from django import forms
from .models import Person


class PersonRegistrationForm(forms.ModelForm):
    """Public registration form - simplified fields."""
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'notification_preference']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+233XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'notification_preference': forms.Select(attrs={'class': 'form-select'}),
        }


class PersonAdminForm(forms.ModelForm):
    """Admin form - all fields available."""
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'notification_preference', 'is_active', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notification_preference': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ExcelImportForm(forms.Form):
    """Form for uploading Excel file to import people."""
    excel_file = forms.FileField(
        label='Excel File',
        help_text='Upload an Excel file (.xlsx) with columns: Name, Country (optional), Contact',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls',
        })
    )
