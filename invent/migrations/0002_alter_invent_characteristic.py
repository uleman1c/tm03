# Generated by Django 4.0.1 on 2022-08-21 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_warehouses_sname'),
        ('invent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invent',
            name='characteristic',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.characteristics'),
        ),
    ]
