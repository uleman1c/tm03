import json
import uuid
from datetime import datetime

from django.db import models

from products.models import *
from users1c.models import Users1c


class Invent(models.Model):
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE)
    warehouse_cell = models.ForeignKey(WarehouseCells, on_delete=models.CASCADE, null=True, default=None, blank=True)

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristics, on_delete=models.CASCADE, null=True, default=None, blank=True)

    quantity = models.DecimalField(max_digits=15, decimal_places=3, default=0)

    comments = models.TextField(blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    id1c = models.CharField(max_length=40, default='')

    delivered_1c = models.BooleanField(default=False);
    is_deleted = models.BooleanField(default=False);

    def __str__(self):
        return "Инвентаризация № %s от %s, %s" % (self.id, self.created, self.warehouse.name)

    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризации'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id1c == '':
            self.id1c = uuid.uuid1()

        super(Invent, self).save(force_insert, force_update, using, update_fields)
