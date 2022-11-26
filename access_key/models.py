import json
from tokenize import blank_re
import uuid
from datetime import datetime

from django.db import models

from users1c.models import Users1c


class AccessKey(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    id1c = models.CharField(max_length=40, default='', blank=True)
    comments = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return "Ключ доступа № %s от %s" % (self.id, self.created)

    class Meta:
        verbose_name = 'Ключ доступа'
        verbose_name_plural = 'Ключи доступа'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id1c == '':
            self.id1c = uuid.uuid4()

        super(AccessKey, self).save(force_insert, force_update, using, update_fields)
