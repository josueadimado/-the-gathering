from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_type', 'person', 'is_anonymous', 'status', 'submitted_at')
    list_filter = ('feedback_type', 'status', 'is_anonymous', 'submitted_at')
    search_fields = ('message', 'person__first_name', 'person__last_name')
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Feedback Information', {
            'fields': ('person', 'feedback_type', 'message', 'is_anonymous')
        }),
        ('Status', {
            'fields': ('status', 'reviewed_at', 'reviewed_by', 'admin_notes')
        }),
    )

