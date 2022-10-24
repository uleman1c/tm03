from django.contrib import admin

import accept_cash
from RequestHeaders.models import *
from invent.models import Invent


class InventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Invent._meta.fields]

    search_fields = [field.name for field in Invent._meta.fields]

    class Meta:
        model = Invent


admin.site.register(Invent, InventAdmin)
