from django.contrib import admin
from .models import *

class BitrixQueueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BitrixQueue._meta.fields]
    search_fields = [field.name for field in BitrixQueue._meta.fields]
    class Meta:
        model = BitrixQueue

admin.site.register(BitrixQueue)
