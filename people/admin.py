from django.contrib import admin
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'date_registered', 'is_active')
    list_filter = ('is_active', 'date_registered')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    readonly_fields = ('id', 'date_registered')

