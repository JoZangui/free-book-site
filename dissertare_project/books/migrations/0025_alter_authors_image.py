# Generated by Django 4.2.16 on 2024-11-22 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_alter_authors_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Imagem do autor'),
        ),
    ]