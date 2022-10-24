from django.db import models

class Task(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    error_text = models.TextField(max_length=1000)

    def __str__(self):
        return self.error_text

