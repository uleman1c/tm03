import json
import uuid
from datetime import datetime

from django.db import models

from users1c.models import Users1c


class File(models.Model):
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)

    idname = models.CharField(max_length=40, default='')

    name = models.TextField(blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)

    size = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False);
    is_folder = models.BooleanField(default=False);
    parent_id = models.CharField(max_length=40, default='');

    def __str__(self):
        return "Файл № %s от %s, %s" % (self.id, self.created, self.name)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
             
        if self.idname == '':
            self.idname = uuid.uuid1()

        super(File, self).save(force_insert, force_update, using, update_fields)


class FilePart(models.Model):

    file = models.ForeignKey(File, on_delete=models.CASCADE)

    idname = models.CharField(max_length=40, default='')

    number = models.DecimalField(max_digits=5, decimal_places=0, default=0)

    size = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Часть файлов № %s от %s, %s" % (self.number, self.created, self.file.name)

    class Meta:
        verbose_name = 'Часть файлов'
        verbose_name_plural = 'Части файлов'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
             
        if self.idname == '':
            self.idname = uuid.uuid1()

        super(FilePart, self).save(force_insert, force_update, using, update_fields)


