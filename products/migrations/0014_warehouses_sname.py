# Generated by Django 4.0.1 on 2022-08-21 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_remove_warehouses_sname'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouses',
            name='sname',
            field=models.CharField(blank=True, default=None, max_length=255),
        ),
    ]
