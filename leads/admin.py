from django.contrib import admin
from RequestHeaders.models import *
from error_log.models import ErrorLog


class ErrorLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ErrorLog._meta.fields]
    search_fields = [field.name for field in ErrorLog._meta.fields]
    class Meta:
        model = ErrorLog


admin.site.register(ErrorLog, ErrorLogAdmin)
