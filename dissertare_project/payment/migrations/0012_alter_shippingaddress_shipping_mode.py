# Generated by Django 4.2.16 on 2024-12-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_alter_shippingaddress_shipping_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_mode',
            field=models.CharField(default='Enviar', max_length=50, verbose_name='Local de entrega'),
        ),
    ]