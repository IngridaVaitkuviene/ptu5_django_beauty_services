# Generated by Django 4.1.3 on 2022-12-01 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_services', '0002_order_alter_beautysalon_options_orderline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beautysalon',
            name='address',
            field=models.CharField(max_length=100, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='beautysalon',
            name='salon_name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
    ]
