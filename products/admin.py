from django.contrib import admin
from .models import *


class ProductsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Products._meta.fields]
    search_fields = ['article', 'name', 'fullname', 'sfullname', 'id1c']

    class Meta:
        model = Products

class CharacteristicsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Characteristics._meta.fields]

    class Meta:
        model = Characteristics

class WarehousesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Warehouses._meta.fields]

    class Meta:
        model = Warehouses

class WarehouseCellsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WarehouseCells._meta.fields]

    class Meta:
        model = WarehouseCells


admin.site.register(Products, ProductsAdmin)
admin.site.register(Filters)
admin.site.register(Characteristics, CharacteristicsAdmin)
admin.site.register(Warehouses, WarehousesAdmin)
admin.site.register(WarehouseCells, WarehouseCellsAdmin)
