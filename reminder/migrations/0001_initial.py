# Generated by Django 4.1.2 on 2022-11-09 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0007_uploadllink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(blank=True, default=None, null=True)),
                ('remind', models.DateTimeField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file.file')),
            ],
            options={
                'verbose_name': 'Напоминалка',
                'verbose_name_plural': 'Напоминалки',
            },
        ),
    ]
