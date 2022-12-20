from django.db import models
from django.contrib.auth.models import User

from products.models import Warehouses


class Users1c(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    id1c = models.CharField(max_length=40, blank=True)
    idbitrix = models.IntegerField(default=0)
    webhook = models.CharField(max_length=255, blank=True)
    dmbase = models.CharField(max_length=255, blank=True)
    dmuser = models.CharField(max_length=255, blank=True)
    dmbase2 = models.CharField(max_length=255, blank=True)
    dmuser2 = models.CharField(max_length=255, blank=True)
    invent_enabled = models.BooleanField(default=False)
    files_enabled = models.BooleanField(default=False)
    recipes_enabled = models.BooleanField(default=False)
    acceptcash_enabled = models.BooleanField(default=False)
    bitrix_enabled = models.BooleanField(default=False)
    orders_enabled = models.BooleanField(default=False)
    leftovers_enabled = models.BooleanField(default=False)
    warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE, blank=True, null=True)
    outcome_enabled = models.BooleanField(default=False)
    recipe_orders_enabled = models.BooleanField(default=False)
    container_statuses_enabled = models.BooleanField(default=False)
    container_statuses_edit_enabled = models.BooleanField(default=False)

    telegram_id = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Users1c, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ContainerFilesInfoBotUser(models.Model):
    
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)


class UserWarehouse(models.Model):

    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE)

    
class UserOutcomeWarehouse(models.Model):

    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE)

    