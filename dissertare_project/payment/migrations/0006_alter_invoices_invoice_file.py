# Generated by Django 4.2.7 on 2024-09-27 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_alter_invoices_options_alter_invoices_invoice_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='invoice_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
