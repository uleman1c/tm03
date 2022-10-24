from django.contrib import admin
from RequestHeaders.models import *
from tsd_log.models import TsdLog


class TsdLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TsdLog._meta.fields]

    class Meta:
        model = TsdLog


admin.site.register(TsdLog, TsdLogAdmin)
