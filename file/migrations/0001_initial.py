# Generated by Django 4.0.1 on 2022-10-08 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users1c', '0009_users1c_files_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idname', models.CharField(default='', max_length=40)),
                ('name', models.TextField(blank=True, default=None, null=True)),
                ('comments', models.TextField(blank=True, default=None, null=True)),
                ('size', models.DecimalField(decimal_places=0, default=0, max_digits=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users1c.users1c')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
    ]
