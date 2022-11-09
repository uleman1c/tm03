from django.db import models

from file.models import File
from users1c.models import Users1c

# Create your models here.

class Reminder(models.Model):

    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)

    file = models.ForeignKey(File, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=None)

    remind = models.DateTimeField()

    def __str__(self):
        return "Напоминалка"

    class Meta:
        verbose_name = 'Напоминалка'
        verbose_name_plural = 'Напоминалки'


 


