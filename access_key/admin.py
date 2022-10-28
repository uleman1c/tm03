from django.contrib import admin

import block_schema
from RequestHeaders.models import *
from access_key.models import AccessKey


class AccessKeyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AccessKey._meta.fields]

    search_fields = [field.name for field in AccessKey._meta.fields]

    class Meta:
        model = AccessKey


admin.site.register(AccessKey, AccessKeyAdmin)
