# Generated by Django 4.0.1 on 2022-08-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_warehouses_sname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouses',
            name='sname',
            field=models.CharField(blank=True, default=None, max_length=255),
        ),
    ]
