from django.contrib import admin
from .models import MessageTemplate, MessageLog


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'message_type', 'is_active', 'created_at')
    list_filter = ('message_type', 'is_active')
    search_fields = ('name', 'body')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('person', 'event', 'message_type', 'status', 'sent_at', 'created_at')
    list_filter = ('message_type', 'status', 'created_at')
    search_fields = ('person__first_name', 'person__last_name', 'recipient')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

