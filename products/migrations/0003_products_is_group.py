# Generated by Django 4.0.1 on 2022-01-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_filters'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_group',
            field=models.BooleanField(default=False),
        ),
    ]