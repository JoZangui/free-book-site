# Generated by Django 4.2.16 on 2024-12-23 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0032_announcement_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='description',
            field=models.TextField(max_length=100, verbose_name='Descrição'),
        ),
    ]
