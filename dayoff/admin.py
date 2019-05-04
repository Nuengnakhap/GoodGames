from django.contrib import admin

# Register your models here.
from dayoff.models import DayOff


class DayOffAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'type', 'reason', 'date_start', 'date_end', 'approve_status']
    list_editable = ['approve_status']
    list_filter = ['created_by', 'date_start', 'date_end', 'approve_status']
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return []
            else:
                return ['created_by', 'type', 'reason', 'date_start', 'date_end']

admin.site.register(DayOff, DayOffAdmin)