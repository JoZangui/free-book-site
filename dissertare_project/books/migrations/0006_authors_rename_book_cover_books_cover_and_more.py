# Generated by Django 4.1 on 2022-08-28 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_books_book_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nome do autor')),
                ('biography', models.TextField(max_length=400, verbose_name='Biografia do autor')),
            ],
        ),
        migrations.RenameField(
            model_name='books',
            old_name='book_cover',
            new_name='cover',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='book_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='book_file',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='book_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='book_owner',
            new_name='upload_by',
        ),
    ]
