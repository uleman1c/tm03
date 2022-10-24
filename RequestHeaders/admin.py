from django.contrib import admin
from RequestHeaders.models import *


class RequestHeadersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RequestHeaders._meta.fields]

    class Meta:
        model = RequestHeaders


admin.site.register(RequestHeaders, RequestHeadersAdmin)
