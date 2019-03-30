from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from json import dumps

from core.forms import BookChoosing
from catalog.models import Author

from .settings import error_messages


def select(request):
    if request.POST:
        status, response = 500, "Error: internal server error."
        if 'author_id' in request.POST and request.POST['author_id']:
            if 'book_id' in request.POST and request.POST['book_id']:
                form = BookChoosing(request.POST)
                if form.is_valid():
                    print('OK!')
                    return redirect('editor:main', form.cleaned_data['book'])
            else:
                # ok, user chose the author, so we should give a set of related books:
                try:
                    author = Author.objects.get(id=int(request.POST['author_id']))
                except ObjectDoesNotExist:
                    status, response = 404, error_messages['author']
                else:
                    status, response = 200, dumps(author.book_set.all())
        return HttpResponse(response, status=status, content_type='text/plain')
    else:
        form = BookChoosing()
    return render(request, 'core/editor/select.html', {'form': form})


def main(request, book_id):
    # TODO: load data by requested book_id
    # return HttpResponse('NOT IMPLEMENTED BLEAD')
    data = book_id
    return render(request, 'core/editor/main.html', {'data': data})


def symbols(request):
    # TODO: realize api functionality here
    return HttpResponse(dumps({'symbols': 'not realized yet'}), status=200, content_type='text/plain')


def addresses(request):
    # TODO: realize api functionality here
    return HttpResponse(dumps({'addresses': 'not realized yet'}), status=200, content_type='text/plain')
