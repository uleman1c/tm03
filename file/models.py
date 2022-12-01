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
    is_deleted = models.BooleanField(default=False)
    is_folder = models.BooleanField(default=False)
    parent_id = models.CharField(max_length=40, default='')

    def __str__(self):
        return "Файл № %s от %s, %s" % (self.id, self.created, self.name)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
             
        if self.idname == '':
            self.idname = uuid.uuid4()

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
            self.idname = uuid.uuid4()

        super(FilePart, self).save(force_insert, force_update, using, update_fields)


class ExternalLink(models.Model):

    file = models.ForeignKey(File, on_delete=models.CASCADE)

    idname = models.CharField(max_length=40, default='')

    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Внешняя ссылка от %s, %s" % (self.created, self.file.name)

    class Meta:
        verbose_name = 'Внешняя ссылка'
        verbose_name_plural = 'Внешние ссылки'


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
             
        if self.idname == '':
            self.idname = uuid.uuid4()

        super(ExternalLink, self).save(force_insert, force_update, using, update_fields)


class UploadlLink(models.Model):

    file = models.ForeignKey(File, on_delete=models.CASCADE)

    idname = models.CharField(max_length=40, default='')

    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Ссылка загрузки от %s, %s" % (self.created, self.file.name)

    class Meta:
        verbose_name = 'Ссылка загрузки'
        verbose_name_plural = 'Ссылки загрузки'


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
             
        if self.idname == '':
            self.idname = uuid.uuid4()

        super(UploadlLink, self).save(force_insert, force_update, using, update_fields)

class FileOwner(models.Model):

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)

    idname = models.CharField(max_length=40, default='')

    type = models.CharField(max_length=40, default='')
    name = models.CharField(max_length=150, default='')

    comments = models.TextField(blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "Владелец файла № %s %s.%s" % (self.id, self.type, self.name)

    class Meta:
        verbose_name = 'Владелец файла'
        verbose_name_plural = 'Владельцы файлов'


class FileVersion(models.Model):

    version_id = models.CharField(max_length=40, default='')

    number = models.DecimalField(max_digits=5, decimal_places=0, default=0)

    file_id = models.CharField(max_length=40, default='')

    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "Версия файла № %s %s.%s" % (self.number, self.file_id, self.version_id)

    class Meta:
        verbose_name = 'Версия файла'
        verbose_name_plural = 'Версии файлов'

