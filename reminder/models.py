from django.db import models

from file.models import File

# Create your models here.

class Reminder(models.Model):

    file = models.ForeignKey(File, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=None)

    remind = models.DateTimeField()

    def __str__(self):
        return "Напоминалка"

    class Meta:
        verbose_name = 'Напоминалка'
        verbose_name_plural = 'Напоминалки'


 


