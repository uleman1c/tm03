from django.contrib import admin
from .models import *


class Users1cAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Users1c._meta.fields]
    search_fields = [field.name for field in Users1c._meta.fields]

    class Meta:
        model = Users1c

class ContainerFilesInfoBotUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContainerFilesInfoBotUser._meta.fields]
    search_fields = [field.name for field in ContainerFilesInfoBotUser._meta.fields]

    class Meta:
        model = ContainerFilesInfoBotUser


class UserWarehouseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserWarehouse._meta.fields]
    search_fields = [field.name for field in UserWarehouse._meta.fields]

    class Meta:
        model = UserWarehouse


admin.site.register(Users1c, Users1cAdmin)
admin.site.register(ContainerFilesInfoBotUser, ContainerFilesInfoBotUserAdmin)
admin.site.register(UserWarehouse, UserWarehouseAdmin)

