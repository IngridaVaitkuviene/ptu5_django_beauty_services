# Generated by Django 4.1.3 on 2022-12-02 17:37

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_services', '0003_alter_beautysalon_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ('user',), 'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='salonservice',
            options={'ordering': ('service',)},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('service_type', 'service_name'), 'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.AddField(
            model_name='beautysalon',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='description'),
        ),
    ]
