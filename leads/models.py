from django.db import models

class Lead(models.Model):
    lead_id = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

