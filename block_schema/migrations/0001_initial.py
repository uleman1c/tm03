# Generated by Django 4.1.2 on 2022-10-28 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema', models.TextField(blank=True, default=None, null=True)),
                ('created', models.DateTimeField()),
                ('id1c', models.CharField(default='', max_length=40)),
            ],
            options={
                'verbose_name': 'Блок-схема',
                'verbose_name_plural': 'Блок-схемы',
            },
        ),
    ]
