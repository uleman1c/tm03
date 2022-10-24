from django.contrib import admin

import contractors
from RequestHeaders.models import *
from contractors.models import Contractors


class ContractorsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contractors._meta.fields]

    search_fields = [field.name for field in Contractors._meta.fields]

    class Meta:
        model = Contractors


admin.site.register(Contractors, ContractorsAdmin)
