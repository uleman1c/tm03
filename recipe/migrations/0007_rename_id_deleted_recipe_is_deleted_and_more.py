# Generated by Django 4.1.2 on 2022-11-27 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_recipeorder_recipe_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='id_deleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='recipeorder',
            old_name='id_deleted',
            new_name='is_deleted',
        ),
    ]