from django.db import models


class Contractors(models.Model):
    name = models.CharField(max_length=255)
    sname = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)
    kpp = models.CharField(max_length=10)
    id1c = models.CharField(max_length=40)

    def __str__(self):
        return self.name
