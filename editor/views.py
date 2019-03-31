from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from json import dumps

from core.forms import BookChoosing
from catalog.models import Author, Book

from .settings import error_messages


def select(request, method):
    if method == 'ajax':
        status, response = 500, "Error: internal server error."
        if request.POST:
            if 'author' in request.POST and request.POST['author']:
                # ok, user chose the author, so we should give a set of related books:
                try:
                    author = Author.objects.get(id=int(request.POST['author']))
                except ObjectDoesNotExist:
                    status, response = 404, error_messages['author']
                else:
                    status, response = 200, dumps({i: t for i, t in author.book_set.values_list('id', 'title')},
                                                  ensure_ascii=False)
        return HttpResponse(response, status=status, content_type='application/json')
    else:
        if request.POST and 'author' in request.POST and 'book' in request.POST:
            form = BookChoosing(request.POST)
            if form.is_valid():
                print('OK!')
                return redirect('editor:main', form.cleaned_data['book'])
        else:
            form = BookChoosing()
        return render(request, 'core/editor/select.html', {'form': form})


def main(request, book_id):
    # TODO: load data by requested book_id
    data = get_object_or_404(Book, id=book_id)
    return render(request, 'core/editor/main.html', {'data': data})


def symbols(request):
    # TODO: realize api functionality here
    return HttpResponse(dumps({'symbols': 'not realized yet'}), status=200, content_type='text/plain')


def addresses(request):
    # TODO: realize api functionality here
    return HttpResponse(dumps({'addresses': 'not realized yet'}), status=200, content_type='text/plain')
