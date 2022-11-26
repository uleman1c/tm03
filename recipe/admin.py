from django.contrib import admin

from recipe.models import RecipeOrder, Recipe, RecipeGoods


class RecipeOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RecipeOrder._meta.fields]

    class Meta:
        model = RecipeOrder

class RecipeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Recipe._meta.fields]

    class Meta:
        model = Recipe

class RecipeGoodsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RecipeGoods._meta.fields]

    class Meta:
        model = RecipeGoods



admin.site.register(RecipeOrder, RecipeOrderAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeGoods, RecipeGoodsAdmin)

