import json
import uuid
from datetime import datetime

from django.db import models

from contractors.models import Contractors
from currency.models import Currency
from users1c.models import Users1c


class AcceptCash(models.Model):
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for all products in order

    comments = models.TextField(blank=True, null=True, default=None)
    order_number = models.CharField(max_length=15, default=None)
    order_date = models.DateTimeField(default=datetime(1970, 1, 1))

    created = models.DateTimeField()
    id1c = models.CharField(max_length=40, default='')

    delivered1c = models.BooleanField(default=False);
    id_deleted = models.BooleanField(default=False);

    def __str__(self):
        return "Получение денег № %s от %s, %s" % (self.id, self.created, self.contractor.name)

    class Meta:
        verbose_name = 'Получение денег'
        verbose_name_plural = 'Получение денег'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id1c == '':
            self.id1c = uuid.uuid4()

        super(AcceptCash, self).save(force_insert, force_update, using, update_fields)
