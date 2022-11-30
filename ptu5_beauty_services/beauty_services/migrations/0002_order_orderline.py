# Generated by Django 4.1.3 on 2022-11-30 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='order date')),
                ('total_sum', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='total sum')),
                ('reserved_date', models.DateField(blank=True, null=True, verbose_name='reserved date')),
                ('status', models.CharField(choices=[('n', 'new'), ('a', 'advance payment taken'), ('c', 'cancelled'), ('p', 'paid'), ('d', 'done')], default='n', max_length=1, verbose_name='status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='beauty_services.customer', verbose_name='customer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_lines', to='beauty_services.order', verbose_name='order')),
                ('salon_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_lines', to='beauty_services.salonservice', verbose_name='salon service')),
            ],
            options={
                'verbose_name': 'Order line',
                'verbose_name_plural': 'Order lines',
            },
        ),
    ]
