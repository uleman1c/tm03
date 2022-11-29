# Generated by Django 4.1.2 on 2022-11-14 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_warehousecells'),
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
            options={
                'verbose_name': 'Товар в рецепте',
                'verbose_name_plural': 'Товары в рецепте',
            },
        ),
    ]