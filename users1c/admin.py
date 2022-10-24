from django.contrib import admin
from .models import *


class Users1cAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Users1c._meta.fields]
    search_fields = [field.name for field in Users1c._meta.fields]

    class Meta:
        model = Users1c


admin.site.register(Users1c, Users1cAdmin)
