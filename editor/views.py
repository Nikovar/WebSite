from collections import defaultdict
from json import dumps
from math import ceil

from django.db import transaction
from django.db.models import F, IntegerField, Q, Sum
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import guest_account
from catalog.models import Author, Book, Existence, Location, Symbol, Context, ContextType
from catalog.utils import get_text
from core.forms import BookChoosing

from .settings import BOOK_CHUNK_SIZE, error_messages


def select_book(request, method):
    if method == 'ajax':
        status, response = 500, "Error: internal server error."
        if request.POST:
            if 'author' in request.POST and request.POST['author']:
                # ok, user chose the author, so we should give a set of related books:
                try:
                    author = Author.objects.get(id=int(request.POST['author']))
                except Author.DoesNotExist:
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
        return render(request, 'editor/select_book.html', {'form': form})


def main(request, book_id):
    # TODO: Обработать ситуацию, когда нет нужной книги. 
    # Можно просто в интерфейсе вывести div с соответствующим сообщением
    book = get_object_or_404(Book, id=book_id)
    context = _get_book_data(request, book)
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id
    # get checked or added by user itself symbols
    symbols = book.symbol_set.exclude(Q(checked=False) & ~Q(inserter_id=user_id)).values('id', 'name')
    
    context['symbols'] = [{
        'value': symbol['id'],
        'label': symbol['name']
    } for symbol in symbols]

    return render(request, 'editor/main.html', context)


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
    except AssertionError:
        return HttpResponse('""', content_type='application/json')

    return JsonResponse({'status': True, 'data': context}, safe=False)


# TODO: check whether this works with new param `checked`
def symbols(request):
    book_id = request.GET.get('book_id')
    q = request.GET.get('q')  # то, что ввёл пользователь (часть названия символа)
    book = Book.objects.get(id=book_id)

    user_id = None
    if request.user.is_authenticated():
        user_id = request.user.id

    queried_symbols = book.symbol_set.filter(
        name_contains=q
    ).exclude(
        Q(checked=False) & ~Q(inserter_id=user_id)
    ).values_list('pk', 'name')

    symbols_list = [{
        'value': s.pk,
        'label': s.name,
    } for s in queried_symbols]

    return JsonResponse([], safe=False)


def locations(request):
    symbol_id = request.POST.get('symbol', None)
    book_id = request.POST.get('book', None)
    if symbol_id is None or book_id is None:
        return HttpResponseBadRequest("You should give a required symbol laid in certain book.")
    try:
        symbol_id, book_id = int(symbol_id), int(book_id)
        assert symbol_id >= 1, book_id >= 1  # ">= 1" because of indexes in table start with number 1
        Symbol.objects.get(id=symbol_id)  # only for checking on "DoesNotExist" error

        exis_ids = Book.objects.get(id=book_id).existence_set.filter(symbol_id=symbol_id).values_list('id', flat=True)

        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id
        queried_locations = Location.objects.filter(existence_id__in=exis_ids).exclude(
            Q(checked=False) & ~Q(inserter_id=user_id)
        ).values_list(
            'start', 
            'word_shift',
            'word_len', 
            'end_shift'
        )
        locations_ = list(queried_locations)

    except (TypeError, AssertionError):
        return HttpResponseBadRequest("You should pass correct identifiers.")
    except Book.DoesNotExist:
        return HttpResponseNotFound("Can't find book with id={}".format(book_id))
    except Symbol.DoesNotExist:
        return HttpResponseNotFound("Can't find symbol with id={}".format(symbol_id))

    return JsonResponse({'locations': locations_})


def contexts(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id

    res = [{
        'value': c.pk,
        'label': c.text[:20] + '...' if len(c.text) > 20 else c.text
    } for c in Context.objects.exclude(Q(checked=False) & ~Q(inserter_id=user_id))[:20]]
    return JsonResponse({'result': res})


def context_types(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id

    res = [{
        'value': ct.pk,
        'label': ct.name
    } for ct in ContextType.objects.exclude(Q(checked=False) & ~Q(inserter_id=user_id))[:20]]
    return JsonResponse({'result': res})


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
    user_id = request.user.id if request.user.is_authenticated else None
    locations = Location.objects.filter(existence__book=book).exclude(Q(checked=False) & ~Q(inserter_id=user_id))
    checking = locations.exists()
    text = get_text(book.file)

    text_chunk, locations, start_position = _get_chunk(locations, text, BOOK_CHUNK_SIZE, page, checking)

    if checking:
        query_set = locations.values_list('existence__symbol', 'start', 'word_shift', 'word_len', 'end_shift')

        locations = defaultdict(list)
        for loc in query_set:
            locations[loc[0]].append(list(loc[1:]))

    return {
        'existences': dict(locations),  # чтобы корректно пробрасывать из шаблона в react.
        'text_chunk': text_chunk.replace('\n', ' '), 
        'page': page, 
        'number_pages': ceil(len(text) / BOOK_CHUNK_SIZE),
        'book_id': book.pk,
        'start_position': start_position
    }


# TODO: add storing of context within new symbol... or do it only in `store_context` view
def store_location(request, book_id, *args, **kwargs):

    book = Book.objects.get(pk=book_id)

    symbol_id = request.POST['symbol_id']
    symbol_title = request.POST['symbol_title'].strip().lower()

    with transaction.atomic():
        if symbol_id == 'new':
            symbol, _ = Symbol.objects.get_or_create(name=symbol_title)
        else:
            symbol = Symbol.objects.get(pk=symbol_id)

        if request.user.is_authenticated:   
            inserter = request.user
        else:
            inserter, _ = guest_account(get_id_only=False)

        existence, _ = Existence.objects.get_or_create(symbol=symbol, book=book)
        checked = True if (inserter.is_superuser or inserter.is_staff) else False

        new_loc = Location.objects.create(
            existence=existence,
            start=request.POST['start'],
            end_shift=request.POST['end'],
            word_len=request.POST['word_len'],
            word_shift=request.POST['word_shift'],
            inserter=inserter,
            checked=checked,
        )

        for context_id in request.POST.getlist('context_ids[]'):
            cont = Context.objects.get(pk=context_id)
            new_loc.contexts.add(cont)

        if checked:
            new_loc.who_checked = inserter
            new_loc.date_checked = new_loc.date_joined
            new_loc.save()

    # Ответ оставить пока именно в таком виде. Нам пока нет нужды ещё что-то возвращать.
    return JsonResponse({'status': True}, safe=False)


def store_context(request, book_id):
    if request.user.is_authenticated:   
        inserter = request.user
    else:
        inserter, _ = guest_account(get_id_only=False)

    checked = True if (inserter.is_superuser or inserter.is_staff) else False
    type_id = request.POST.get('context_type')
    text = request.POST.get('context_description', '').strip()

    if type_id and text:
        new_context = Context.objects.create(type_id=type_id, text=text, inserter=inserter, checked=checked)
        new_loc.contexts.add(new_context)
        if checked:
            new_context.who_checked = inserter
            new_context.date_checked = new_loc.date_joined
            new_context.save()
    
    return JsonResponse({'status': True}, safe=False)
