from django.contrib import admin

from recipe.models import Recipe, RecipeGoods


class RecipeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Recipe._meta.fields]

    class Meta:
        model = Recipe

class RecipeGoodsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RecipeGoods._meta.fields]

    class Meta:
        model = RecipeGoods



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeGoods, RecipeGoodsAdmin)

