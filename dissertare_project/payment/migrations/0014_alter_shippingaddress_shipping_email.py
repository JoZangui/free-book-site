# Generated by Django 4.2.16 on 2024-12-11 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_invoices_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_email',
            field=models.EmailField(max_length=255),
        ),
    ]