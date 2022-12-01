# Generated by Django 4.1.2 on 2022-12-01 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users1c', '0017_users1c_container_statuses_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='users1c',
            name='telegram_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ContainerFilesInfoBotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users1c.users1c')),
            ],
        ),
    ]
