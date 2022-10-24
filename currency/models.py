import json
import uuid
from datetime import datetime

from django.db import models

from contractors.models import Contractors
from users1c.models import Users1c


class Currency(models.Model):
    code = models.CharField(max_length=3, default=None)
    name = models.CharField(max_length=30, default=None)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

