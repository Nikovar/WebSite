from json import dumps
from functools import reduce

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum, IntegerField
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from catalog.models import Author, Book, Location, Symbol
from catalog.utils import get_text

from core.forms import BookChoosing
from .settings import error_messages, BOOK_CHUNK_SIZE


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
                return redirect('editor:main', form.cleaned_data['book'])
        else:
            form = BookChoosing()
        return render(request, 'core/editor/select.html', {'form': form})


def main(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = _get_data(request, book)

    qs = book.symbol_set.annotate(descr=F('description__text')).values_list('id', 'name', 'descr')
    symbs = {tup[0]: tup[1:] for tup in qs}

    context['symbols'] = symbs
    # TODO: remove 'main_test' from there...
    # return render(request, 'core/editor/main.html', context)
    return render(request, 'core/editor/main_test.html', context)


def get_page(request):
    book_id = request.POST.get('book', None)
    page_num = request.POST.get('page', None)
    if book_id is None or page_num is None:
        return HttpResponseBadRequest("You should pass identifier of certain book with required page in it.")
    try:
        book_id, page_num = int(book_id), int(page_num)
        assert book_id >= 1, page_num >= 0
        book = Book.objects.get(id=book_id)
    except (TypeError, AssertionError):
        return HttpResponseBadRequest("You should pass correct book identifier and page number.")
    except Book.DoesNotExist:
        return HttpResponseNotFound("Can't find book by passed identifier.")

    try:
        context = _get_data(request, book, page_num)
    except AssertionError:
        return HttpResponse('""', content_type='application/json')
    return HttpResponse(dumps(context), content_type='application/json')


# Commented this because of all related symbols we already pass in "main" view. So i don't know if this needed.
# def symbols(request):
#     qs = Symbol.objects.annotate(descr=F('description__text')).values_list('id', 'name', 'descr')
#     all_symbols = {tup[0]: tup[1:] for tup in qs}
#     return HttpResponse(dumps({'symbols': all_symbols}), content_type='application/json')


def symbols(request):
    # TODO: realize api functionality here

    # "Поправил" вьюху для теста. В value нужно будет сувать id символа
    # в label - его название

    book_id = request.GET.get('book_id')
    q = request.GET.get('q')  # то, что ввёл пользователь (часть названия символа)

    test_symbols = [
        {
            'value': 1,
            'label': 'Elephant'
        },
        {
            'value': 2,
            'label': 'Dog',
        },
        {
            'value': 3,
            'label': 'Oil'
        }
    ]

    result = [symbol for symbol in test_symbols if q in symbol['label']]
    return JsonResponse(result, safe=False)


def addresses(request):
    symbol_id = request.POST.get('symbol', None)
    book_id = request.POST.get('book', None)
    if symbol_id is None or book_id is None:
        return HttpResponseBadRequest("You should give a required symbol laid in certain book.")
    try:
        symbol_id, book_id = int(symbol_id), int(book_id)
        assert symbol_id >= 1, book_id >= 1  # ">= 1" because of indexes in table start with number 1
        Symbol.objects.get(id=symbol_id)  # only for checking on "DoesNotExist" error

        exis_ids = Book.objects.get(id=book_id).existence_set.filter(symbol_id=symbol_id).values_list('id', flat=True)
        qs = Location.objects.filter(existence_id__in=exis_ids).order_by('start').values_list('start', 'word_shift',
                                                                                              'word_len', 'end_shift')
        adrs = list(qs)
    except (TypeError, AssertionError):
        return HttpResponseBadRequest("You should pass correct identifiers.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Can't find objects by passed identifiers.")

    return HttpResponse(dumps({'locations': adrs}), content_type='application/json')


def _check_crossing(board, addrs, is_left):
    crossed = addrs.filter(start__lte=board, end_shift__gt=board - F('start'))
    if len(crossed) == 0:
        return None
    crossed = crossed.annotate(_board=Sum(F('start') + F('end_shift') - board, output_field=IntegerField()))
    order_field = '_board' if is_left else '-_board'
    furthest = crossed.order_by(order_field)[0]
    return furthest.start + furthest.end_shift if is_left else furthest.start


def _get_chunk(adrs, text, chunk_size, page):
    left_right = [page * chunk_size, (page + 1) * chunk_size]
    assert left_right[0] < len(text)

    for i, board in enumerate(left_right):
        if board != 0 and board != len(text):
            new_board = _check_crossing(board, adrs, bool(i))
            if new_board is not None:
                left_right[i] = new_board
    left, right = left_right
    adrs = adrs.filter(start__gte=left, end_shift__lte=right - F('start'))
    return text[left: right], adrs


def _get_data(request, book, page=0):
    text = get_text(book.file)

    prefetch_related_objects([book], 'existence_set')
    adrs = reduce(lambda x, y: x | y, [existence.locations.all() for existence in book.existence_set.all()])
    chunk, adrs = _get_chunk(adrs, text, BOOK_CHUNK_SIZE, page)

    qs = adrs.annotate(symb=F('existence__symbol')).order_by('start').values_list('symb', 'start', 'word_shift',
                                                                                  'word_len', 'end_shift')
    adrs = {tup[0]: tup[1:] for tup in qs}
    return {'existences': adrs, 'text': chunk, 'page': page}

