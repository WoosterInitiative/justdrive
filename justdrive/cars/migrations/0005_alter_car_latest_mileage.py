# Generated by Django 3.2.15 on 2022-10-03 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_car_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='latest_mileage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='latest reported mileage'),
        ),
    ]
