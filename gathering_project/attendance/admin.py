from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('person', 'event', 'check_in_time', 'check_in_method', 'checked_in_by')
    list_filter = ('check_in_method', 'check_in_time', 'event')
    search_fields = ('person__first_name', 'person__last_name', 'person__phone_number', 'event__name')
    date_hierarchy = 'check_in_time'
    readonly_fields = ('check_in_time',)

