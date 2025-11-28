from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'event_date', 'event_time', 'event_type', 'location', 'is_active')
    list_filter = ('event_type', 'is_active', 'event_date')
    search_fields = ('name', 'topic', 'location', 'description')
    date_hierarchy = 'event_date'
    readonly_fields = ('created_at', 'updated_at')

