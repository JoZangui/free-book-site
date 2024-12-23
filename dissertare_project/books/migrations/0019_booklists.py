# Generated by Django 4.2.16 on 2024-11-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0018_remove_books_category_books_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=50, verbose_name='Nome da lista')),
                ('list_description', models.TextField(verbose_name='Descrição da lista')),
                ('books', models.ManyToManyField(to='books.books', verbose_name='Livros')),
            ],
        ),
    ]
