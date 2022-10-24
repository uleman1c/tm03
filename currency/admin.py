from django.contrib import admin

import accept_cash
from RequestHeaders.models import *
from accept_cash.models import AcceptCash
from currency.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Currency._meta.fields]
    search_fields = [field.name for field in Currency._meta.fields]
    
    class Meta:
        model = Currency


admin.site.register(Currency, CurrencyAdmin)
