# Generated by Django 4.0.1 on 2022-10-09 06:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_filepart'),
    ]

    operations = [
        migrations.AddField(
            model_name='filepart',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
