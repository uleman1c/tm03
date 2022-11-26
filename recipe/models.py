from django.db import models

import json
import uuid
from datetime import datetime

from django.db import models

from contractors.models import Contractors
from currency.models import Currency
from products.models import Characteristics, Products
from users1c.models import Users1c


class RecipeOrder(models.Model):
    
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=None)
    end_product = models.ForeignKey(Products, blank=True, null=True, default=None, on_delete=models.CASCADE)
    end_product_text = models.TextField(blank=True, null=True, default=None)
    color_number = models.CharField(max_length=15, default=None)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    id1c = models.CharField(max_length=40, default='')

    delivered1c = models.BooleanField(default=False)
    id_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "Заявка на рецепт № %s от %s, %s" % (self.id, self.created, self.contractor.name)

    class Meta:
        verbose_name = 'Заявка на рецепт'
        verbose_name_plural = 'Заявка на рецепт'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id1c == '':
            self.id1c = uuid.uuid4()

        super(RecipeOrder, self).save(force_insert, force_update, using, update_fields)

class Recipe(models.Model):

    order = models.ForeignKey(RecipeOrder, blank=True, null=True, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=None)
    end_product = models.ForeignKey(Products, blank=True, null=True, default=None, on_delete=models.CASCADE)
    end_product_text = models.TextField(blank=True, null=True, default=None)
    color_number = models.CharField(max_length=15, default=None)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    id1c = models.CharField(max_length=40, default='')

    delivered1c = models.BooleanField(default=False)
    id_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "Рецепт № %s от %s, %s" % (self.id, self.created, self.contractor.name)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепт'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id1c == '':
            self.id1c = uuid.uuid4()

        super(Recipe, self).save(force_insert, force_update, using, update_fields)

class RecipeGoods(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, blank=True, null=True, default=None, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristics, on_delete=models.CASCADE, null=True, default=None, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в рецепте'
        verbose_name_plural = 'Товары в рецепте'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # price_per_item = self.product.price
        # self.price_per_item = price_per_item
        # self.total_price = int(self.nmb) * price_per_item

        super(RecipeGoods, self).save(force_insert, force_update, using, update_fields)

