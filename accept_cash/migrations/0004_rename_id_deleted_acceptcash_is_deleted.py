# Generated by Django 4.1.2 on 2022-11-27 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accept_cash', '0003_acceptcash_id_deleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acceptcash',
            old_name='id_deleted',
            new_name='is_deleted',
        ),
    ]
