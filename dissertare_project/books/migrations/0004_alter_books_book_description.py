# Generated by Django 4.1 on 2022-08-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_books_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='book_description',
            field=models.TextField(max_length=400, verbose_name='Descrição do livro'),
        ),
    ]
