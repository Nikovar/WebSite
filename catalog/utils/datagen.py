# utility for creating symbol existence in certain book with locations by passed symbol name.

# there is 'regex' outer module, use pip for install it
from regex import finditer

from django.db.models import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from catalog.models import Symbol, Book, Existence, Location
from catalog.utils import get_text


def generate_existence(symbol, book):
    try:
        assert isinstance(symbol, Symbol) and isinstance(book, Book)
    except AssertionError:
        try:
            assert isinstance(symbol, int) and isinstance(book, int)
            symbol_ = Symbol.objects.get(id=symbol)
            book_ = Book.objects.get(id=book)
        except AssertionError:
            raise TypeError("'symbol' and 'book' must be a instances of models or its integer identifiers.") from None
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Can't find objects by identifiers that you passed.") from None
        else:
            symbol, book = symbol_, book_
    text = get_text(book.file)
    new_locations_added = 0
    if _symbol_exists(symbol.name, text):
        staff_user = get_user_model().objects.get_or_create(username='Generator')[0]
        new_ex = Existence.objects.create(symbol=symbol, book=book, inserter=staff_user)

        locations, container = _get_locations(symbol.name, text), {}
        Location.objects.bulk_create([Location(**_pack_location_params(loc, new_ex, container)) for loc in locations])
        new_locations_added = len(locations)
    return new_locations_added


def generate_symbol(symbol_name, book):
    try:
        assert isinstance(symbol_name, str)
    except AssertionError:
        raise TypeError from None

    symbol = Symbol.objects.create(name=symbol_name)
    try:
        assert isinstance(book, Book)
    except AssertionError:
        try:
            assert isinstance(book, int) and book > 0
            book_ = Book.objects.get(id=book)
        except AssertionError:
            raise TypeError("You should pass book model instance or pk of some book.") from None
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Can't find book by passed id.") from None
        else:
            book = book_
    return generate_existence(symbol, book)


def _symbol_exists(symbol_name, text):
    return True if text.find(symbol_name) != -1 else False


def _get_locations(symbol_name, text):
    locations = []
    for sentence in finditer(r'(^|[\.\!\?])[\s]*([^\.\!\?]+([\.\!\?]|$))', text, overlapped=True):
        existences = _locator(symbol_name, sentence.group(2))
        if len(existences) == 0:
            continue
        start = sentence.start(2)
        end_shift = sentence.end(2) - start
        sent_locations = [(start, ex[0], ex[1] - ex[0], end_shift) for ex in existences]
        locations += sent_locations
    return locations


def _locator(p, sentence):
    return [x.span() for x in finditer(p, sentence, overlapped=True)]


def _pack_location_params(location, existence, params):
    params['checked'] = True
    params['existence'] = existence
    for loc_value, p_name in zip(location, ('start', 'word_shift', 'word_len', 'end_shift')):
        params[p_name] = loc_value

    return params
