from django.db import models


class Products(models.Model):
    article = models.CharField(max_length=25, blank=True, default=None)
    name = models.CharField(max_length=255)
    fullname = models.TextField(max_length=1000, blank=True, default=None)
    sfullname = models.TextField(max_length=1000, blank=True, default=None)
    is_group = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    id1c = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Characteristics(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    id1c = models.CharField(max_length=40)
    owner_id1c = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

class Warehouses(models.Model):
    name = models.CharField(max_length=255)
    sname = models.CharField(max_length=255, blank=True, default=None)
    is_group = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    id1c = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class WarehouseCells(models.Model):
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    sname = models.CharField(max_length=255, blank=True, default=None)
    section = models.CharField(max_length=3, blank=True, default=None)
    line = models.CharField(max_length=3, blank=True, default=None)
    rack = models.CharField(max_length=5, blank=True, default=None)
    stage = models.CharField(max_length=3, blank=True, default=None)
    position = models.CharField(max_length=2, blank=True, default=None)
    is_group = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    warehouse_id1c = models.CharField(max_length=40)
    id1c = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Складская ячейка'
        verbose_name_plural = 'Складские ячейки'


class Filters(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    text = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.text

