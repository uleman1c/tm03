from django.contrib import admin

import accept_cash
from RequestHeaders.models import *
from accept_cash.models import AcceptCash


class AcceptCashAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AcceptCash._meta.fields]

    search_fields = [field.name for field in AcceptCash._meta.fields]

    class Meta:
        model = AcceptCash


admin.site.register(AcceptCash, AcceptCashAdmin)
