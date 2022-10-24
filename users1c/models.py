from django.db import models
from django.contrib.auth.models import User


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

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Users1c, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
