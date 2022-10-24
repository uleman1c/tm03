from django.db import models

class OrderInfo(models.Model):
    id1c = models.CharField(max_length=40)
    strnum = models.IntegerField()
    product = models.CharField(max_length=255)
    character = models.CharField(max_length=255)
    quantity = models.FloatField()
    quantity1 = models.FloatField()
    quantity2 = models.FloatField()
    quantity3 = models.FloatField()
    quantity4 = models.FloatField()
    quantity5 = models.FloatField()
    comment = models.CharField(max_length=255)


    def __str__(self):
        return self.product

