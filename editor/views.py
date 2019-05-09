from collections import defaultdict
from functools import reduce
from json import dumps
from math import ceil

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.models import F, IntegerField, Sum
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Author, Book, Existence, Location, Symbol, SymbolDescription
from catalog.utils import get_text
from core.forms import BookChoosing

from .settings import BOOK_CHUNK_SIZE, error_messages


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
    # TODO: Обработать ситуацию, когда нет нужной книги. 
    # Можно просто в интерфейсе вывести div с соответствующим сообщением
    book = get_object_or_404(Book, id=book_id)
    context = _get_book_data(request, book)

    symbols = book.symbol_set.values_list('id', 'name', 'descriptions__text')

    tmp_res = defaultdict(lambda: {'name': '', 'descriptions': []})
    for s in symbols:
        tmp_res[s[0]]['name'] = s[1]
        if s[2]:
            tmp_res[s[0]]['descriptions'].append(s[2])

    symbols = [{
        'value': symbol_id,
        'label': symbol_data['name'],
        'descriptions': symbol_data['descriptions']
    } for symbol_id, symbol_data in tmp_res.items()]

    context['symbols'] = symbols
    return render(request, 'core/editor/main.html', context)


def get_page(request, book_id, page):
    if book_id is None or page is None:
        return HttpResponseBadRequest("You should pass identifier of certain book with required page in it.")

    try:
        book_id, page = int(book_id), int(page)
        assert book_id >= 1, page >= 1
        book = Book.objects.get(id=book_id)
    except (TypeError, AssertionError):
        return HttpResponseBadRequest("You should pass correct book identifier and page number.")
    except Book.DoesNotExist:
        return HttpResponseNotFound("Can't find book by passed identifier.")

    try:
        context = _get_book_data(request, book, page)
        print(context['existences'])
    except AssertionError:
        return HttpResponse('""', content_type='application/json')

    return JsonResponse({'status': True, 'data': context}, safe=False)


def symbols(request):
    # "Поправил" вьюху для теста. В value нужно будет сувать id символа
    # в label - его название

    book_id = request.GET.get('book_id')
    q = request.GET.get('q')  # то, что ввёл пользователь (часть названия символа)

    book = Book.objects.get(id=book_id)
    symbols = book.symbol_set.filter(name__contains=q).values_list('id', 'name')

    result = [{
        'value': symbol[0],
        'label': symbol[1],
    } for symbol in symbols]

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
        qs = Location.objects.filter(existence_id__in=exis_ids).order_by('start').values_list(
            'start', 
            'word_shift',
            'word_len', 
            'end_shift'
        )
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


def _get_chunk(adrs, text, chunk_size, page, checking):
    left_right = [(page-1) * chunk_size, page * chunk_size]
    
    assert left_right[0] < len(text)

    for i, board in enumerate(left_right):
        if board != 0 and board != len(text):
            new_board = _check_crossing(board, adrs, bool(i)) if checking else None
            if new_board is not None:
                left_right[i] = new_board
    left, right = left_right

    if checking:
        adrs = adrs.filter(start__gte=left, end_shift__lte=right - F('start'))

    return text[left: right], adrs, left


def _get_book_data(request, book, page=1):

    text = get_text(book.file)
    adrs, checking = {}, False

    prefetch_related_objects([book], 'existence_set')
    all_book_existences = book.existence_set.all()
    if len(all_book_existences) > 0:
        checking = True
        adrs = reduce(lambda x, y: x | y, [existence.locations.all() for existence in all_book_existences])

    text_chunk, adrs, start_position = _get_chunk(adrs, text, BOOK_CHUNK_SIZE, page, checking)

    if checking:
        qs = adrs.order_by('start').values_list('existence__symbol', 'start', 'word_shift', 'word_len', 'end_shift')

        adrs = defaultdict(list)
        for address in qs:
            adrs[address[0]].append(list(address[1:]))

    return {
        'existences': dict(adrs),  # чтобы корректно пробрасывать из шаблона в react.
        'text_chunk': text_chunk.replace('\n', ' '), 
        'page': page, 
        'number_pages': ceil(len(text) / BOOK_CHUNK_SIZE),
        'book_id': book.pk,
        'start_position': start_position
    }


def tmp_save_symbol(request, book_id, *args, **kwargs):
    book = Book.objects.get(pk=book_id)
    author = book.author

    tmp_author, _ = Author.objects.using('temp').get_or_create(
        pk=author.pk,
        first_name=author.first_name,
        last_name=author.last_name,
    )

    tmp_book, _ = Book.objects.using('temp').get_or_create(
        pk=book.pk,
        title=book.title,
        author=tmp_author,
    )
    
    symbol_id = request.POST['symbol_id']
    symbol_title = request.POST['symbol_title'].strip().lower()

    if symbol_id == 'new':
        tmp_symbol = Symbol.objects.using('temp').get_or_create(name=symbol_title)
    else:
        symbol = Symbol.objects.get(pk=symbol_id)
        tmp_symbol, _ = Symbol.objects.using('temp').get_or_create(name=symbol.name)

    description = request.POST['description'].strip()
    if description:
        SymbolDescription.objects.using('temp').create(symbol=tmp_symbol, text=description)

    tmp_existence, _ = Existence.objects.using('temp').get_or_create(symbol=tmp_symbol, book=tmp_book)

    if request.user.pk is not None:
        tmp_inserter, _ = get_user_model().objects.using('temp').get_or_create(username=request.user.username)
    else:
        # на случай, если у нас размечает не авторизованный пользователь
        tmp_inserter, _ = get_user_model().objects.using('temp').get_or_create(username='temp_user')

    Location.objects.using('temp').create(
        existence=tmp_existence,
        start=request.POST['start'],
        end_shift=request.POST['end'],
        word_len=request.POST['word_len'],
        word_shift=request.POST['word_shift'],
        inserter=tmp_inserter
    )

    # Ответ оставить пока именно в таком виде. Нам пока нет нужды ещё что-то возвращать.
    return JsonResponse({'status': True}, safe=False)
