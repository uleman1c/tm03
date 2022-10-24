from django.db import models


class BitrixQueue(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=255, blank=True)
    idbitrix = models.IntegerField(default=0)
    data = models.TextField(max_length=10000)
    executed = models.BooleanField(default=False)

    def __str__(self):
        return self.mode
