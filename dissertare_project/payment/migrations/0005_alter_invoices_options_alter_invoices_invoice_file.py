# Generated by Django 4.2.7 on 2024-09-26 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_invoices_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoices',
            options={'verbose_name_plural': 'Invoices'},
        ),
        migrations.AlterField(
            model_name='invoices',
            name='invoice_file',
            field=models.FilePathField(blank=True, null=True),
        ),
    ]
