# Generated by Django 4.0.3 on 2022-04-01 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users1c', '0003_remove_users1c_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='users1c',
            name='idbitrix',
            field=models.IntegerField(default=0),
        ),
    ]
