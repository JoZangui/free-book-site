# Generated by Django 4.2.16 on 2024-12-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0028_booklists_update_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='Comment',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='Comentário'),
        ),
        migrations.AlterField(
            model_name='books',
            name='description',
            field=models.TextField(max_length=400, verbose_name='Sinopse'),
        ),
    ]