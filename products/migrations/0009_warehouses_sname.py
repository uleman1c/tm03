# Generated by Django 4.0.1 on 2022-08-21 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_warehouses'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouses',
            name='sname',
            field=models.TextField(blank=True, default=None, max_length=255),
        ),
    ]
