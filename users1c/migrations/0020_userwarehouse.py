# Generated by Django 4.1.2 on 2022-12-15 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_warehousecells'),
        ('users1c', '0019_users1c_container_statuses_edit_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users1c.users1c')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.warehouses')),
            ],
        ),
    ]
