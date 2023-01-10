import os

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from .models import Authors, Books
from .forms import AuthorsForm, BookForm
from dissertare_project.settings import BASE_DIR

from .rename_dir import rename_dir


def _user_is_superuser(user):
    """
    retorna True se o usuário
    é um super usuário, se não, retorna False
    """
    return user.is_superuser


def books(request):
    all_books = Books.objects.all().order_by('-date_posted')

    # classe para separar os itens por páginas (8 itens por página)
    pagtr = Paginator(all_books, 8)

    # número da página a ser apresentada
    page_number = request.GET.get('page')
    # objecto com o número e link das páginas
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'books/books.html',
        {
            'books': all_books,
            'page_obj': page_obj,
            'title': 'home'
        }
    )


def book_detail(request, book_id):
    book = Books.objects.get(pk=book_id)

    return render(request, 'books/book_detail.html', {'book': book, 'title': book.title})


@user_passes_test(_user_is_superuser, redirect_field_name='book')
def upload_book(request):
    """ Apenas admin devem usar essa página """
    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES)

        if book_form.is_valid():
            final_form = book_form.save(commit=False)
            final_form.uploaded_by = request.user
            final_form.save()


            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': final_form.pk}
            ))
        else:
            return render(
                request,
                'books/book_create_form.html',
                {
                    'book_form': book_form,
                    'book_form_erros': book_form.errors,
                    'title': 'carregar livro'
                }
            )

    book_form = BookForm()

    return render(
        request,
        'books/book_create_form.html',
        {'book_form': book_form, 'title': 'carregar livro'}
    )


@user_passes_test(_user_is_superuser, redirect_field_name='book')
def update_book(request, book_id):
    """ Apenas admin deven usar essa página """

    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES,
            instance=book)

        if book_form.is_valid():
            book_form.save()

            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': book_id}))

    book_form = BookForm(instance=book)

    title = f'editar livro {book.title}'

    return render(
        request,
        'books/book_create_form.html',
        {'book_form': book_form, 'title': title}
    )


@user_passes_test(_user_is_superuser, redirect_field_name='book')
def delete_book(request, book_id):
    """ Apenas admin deven usar essa página """
    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book.delete()

        return HttpResponseRedirect(reverse('books'))

    title = f'remover o livro {book.title}'

    return render(request, 'books/delete_book_form.html', {'book': book, 'title': title})


@login_required
def download_book(request, book_id):
    book = Books.objects.get(id=book_id)

    return redirect(book.file.url)


@user_passes_test(_user_is_superuser, redirect_field_name='book')
def register_author(request):
    """ Apenas admin devem usar essa página """
    if request.method == 'POST':
        author_form = AuthorsForm(
            request.POST,
            request.FILES)
        
        if author_form.is_valid():
            author_form.save()

            return HttpResponseRedirect(reverse(
                'author-detail',
                kwargs={'author_name': author_form.instance.name}
            ))
        return render(
            request,
            'books/author_registration_form.html',
            {
                'author_form': author_form,
                'author_form_erros': author_form.errors,
                'title': 'Registar novo autor'
            }
        )

    author_form = AuthorsForm()

    return render(
        request,
        'books/author_registration_form.html',
        {'author_form': author_form, 'title': 'Registar novo autor'}
    )


def author_detail(request, author_name):

    author = Authors.objects.get(name=author_name)
    author_books = author.books_set.all().order_by('-date_posted')

    title = author.name

    return render(
        request,
        'books/author_detail.html',
        {
            'author': author,
            'title': title,
            'author_books': author_books[:4]
        }
    )


def all_authors(request):
    """ todos os autores """

    authors = Authors.objects.all().order_by('-registration_date')

    pagtr = Paginator(authors, 14)
    page_number = request.GET.get('page')
    page_obj = pagtr.get_page(page_number)

    title = 'autores'

    return render (
        request,
        'books/all_authors.html',
        {
            'title': title,
            'page_obj': page_obj
        }
    )


def all_author_books(request, author_name):
    """ todos os livros de um autor """

    author = Authors.objects.get(name=author_name)
    author_books = author.books_set.all().order_by('-date_posted')

    pagtr = Paginator(author_books, 8)
    page_number = request.GET.get('page')
    page_obj = pagtr.get_page(page_number)

    title = f"todos os livros de {author.name}"

    return render(
        request,
        'books/all_author_books.html',
        {
            'author': author,
            'title': title,
            'author_books': author_books,
            'page_obj': page_obj
        }
    )


@user_passes_test(_user_is_superuser, redirect_field_name='book')
def author_update(request, author_name):
    """ Apenas admin deven usar essa página """
    author = Authors.objects.get(name=author_name)


    if request.method == 'POST':
        old_dirname = author.name
        path = os.path.abspath(f'{BASE_DIR}/media/authors/images/')

        author_form = AuthorsForm(
            request.POST,
            request.FILES,
            instance=author)

        if author_form.is_valid():
            # new_dirname = author_form.cleaned_data.get('name')
            # rename_dir(path, old_dirname, new_dirname)

            print(author_form.cleaned_data.get('image'))

            author_form.save()

            return HttpResponseRedirect(reverse(
                'author-detail',
                kwargs={'author_name': author.name}))

    author_form = AuthorsForm(instance=author)
    title = f'actualizar autor {author.name}'
    return render(
        request,
        'books/author_registration_form.html',
        {'author_form': author_form, 'title': title})


@user_passes_test(_user_is_superuser, redirect_field_name='book')
def delete_author(request, author_name):
    """ Apenas admin deven usar essa página """
    author = Authors.objects.get(name=author_name)

    if request.method == 'POST':
        author.delete()

        return HttpResponseRedirect(reverse('books'))

    title = f'remover autor {author.name}'
    return render(request, 'books/delete_author_form.html', {'author': author, 'title': title})
