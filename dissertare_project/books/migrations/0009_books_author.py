# Generated by Django 4.1 on 2022-08-31 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_authors_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.authors', verbose_name='Autor do livro'),
            preserve_default=False,
        ),
    ]