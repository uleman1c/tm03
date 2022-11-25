import json
import uuid
from datetime import datetime

from django.db import models

from users1c.models import Users1c


class BlockSchema(models.Model):
    schema = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    id1c = models.CharField(max_length=40, default='')

    def __str__(self):
        return "Блок-схема № %s от %s" % (self.id, self.created)

    class Meta:
        verbose_name = 'Блок-схема'
        verbose_name_plural = 'Блок-схемы'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id1c == '':
            self.id1c = uuid.uuid4()

        super(BlockSchema, self).save(force_insert, force_update, using, update_fields)
