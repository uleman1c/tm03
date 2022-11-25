import uuid

from django.db import models

from contractors.models import Contractors
from products.models import Products
from users1c.models import Users1c


class Order(models.Model):
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE)

    sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for all products in order

    comments = models.TextField(blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    id1c = models.CharField(max_length=40, default='')

    delivered1c = models.BooleanField(default=False);

    def __str__(self):
        return "Заказ № %s от %s, %s" % (self.id, self.created, self.contractor.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.id1c = uuid.uuid4()

        super(Order, self).save(force_insert, force_update, using, update_fields)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, blank=True, null=True, default=None, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # price_per_item = self.product.price
        # self.price_per_item = price_per_item
        # print (self.nmb)
        #
        # self.total_price = int(self.nmb) * price_per_item

        super(ProductInOrder, self).save(force_insert, force_update, using, update_fields)


class ProductInBasket(models.Model):
    user1c = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, blank=True, null=True, default=None, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # price_per_item = self.product.price
        # self.price_per_item = price_per_item
        # self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(force_insert, force_update, using, update_fields)
