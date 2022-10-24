from django.contrib import admin
from RequestHeaders.models import *
from order_info.models import OrderInfo


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderInfo._meta.fields]
    search_fields = [field.name for field in OrderInfo._meta.fields]
    class Meta:
        model = OrderInfo


admin.site.register(OrderInfo, OrderInfoAdmin)
