from django.utils.html import mark_safe

# importing constants and get access to important import of models:
from . import *


def author_render_data(author_model):
    fields = ('id', 'first_name', 'last_name')
    values = []
    for inst in author_model.objects.using('temp').exclude(date_of_birth=None, date_of_death=None):
        values.append(tuple(getattr(inst, f, '') for f in fields))
    return fields, values


def symbol_descr_render_data(model):
    fields = ['id', 'text']
    values = []
    for inst in model.objects.using('temp').all():
        v = list(getattr(inst, f, '') for f in fields)
        v.append(inst.symbol.name)
        values.append(v)
    fields.append('symbol')
    return fields, values


def book_render_data(book_model):
    fields = ['id', 'title', 'author']
    values = []
    for inst in book_model.objects.using('temp').exclude(file=''):
        values.append(tuple(getattr(inst, f, '') for f in fields))
    return fields, values


def symbol_render_data(symbol_model):
    fields = ['id', 'name']
    values = []
    existed_symbols = set(symbol_model.objects.values_list('name', flat=True))
    for inst in Symbol.objects.using('temp').exclude(name__in=existed_symbols):
        v = list(getattr(inst, f, '') for f in fields)
        occ = '; '.join(['{} (id: {})'.format(*book) for book in inst.occurs_in.values_list('title', 'pk')])
        v.append(occ)
        values.append(v)
    fields.append('occurs in book')
    return fields, values


def location_render_data(location_model):
    use_fields = ('start', 'word_shift', 'word_len', 'end_shift')
    span_open = '<span style="color: {}">'.format(LOCATION_WORD_COLOR)
    loc_info, opened_books = None, {}

    values = []
    for inst in location_model.objects.using('temp').all():
        # selecting book file
        book = inst.existence.book
        try:
            if book.file == '':
                book = Book.objects.get(pk=book.id)

            # getting text from book file
            if book.id in opened_books:
                text = opened_books[book.id]
            else:
                with book.file.open('r') as bf:
                    text = opened_books[book.id] = bf.read()

            # getting standard string representation
            loc_info = None
            loc_info = mark_safe('<span style="font-size: 11px;">{}</span>'.format(inst.__str__()))

        except (ValueError, Book.DoesNotExist,  FileNotFoundError):
            # `ValueError` - raise when book.file == ''
            # `Book.DoesNotExist` - raised by `.get()` when it can't find book instance by passed `book.id`
            # FileNotFoundError - xz. write it just like that... maybe someday it will raise)
            if loc_info is None:
                loc_info = mark_safe('<span style="color: red; font-size: 11px;">Can\'t get object\'s data.</span>')
            location = mark_safe('{}Corrupted Book reference or something another went wrong.</span>'.format(span_open))
        except Exception:
            # too board handling for catch exceptions that may occur in strange way inside `inst.__str__()`. Fix if can
            if loc_info is None:
                loc_info = mark_safe('<span style="color: red; font-size: 11px;">Can\'t get object\'s data.</span>')
            location = mark_safe('{}Corrupted Data. Remove or fix it by yourself.</span>')
        else:
            # form information
            s, wsh, wlen, esh = tuple(getattr(inst, x) for x in use_fields)
            sent = text[s: s + esh]
            location = mark_safe(
                ''.join((sent[:wsh],
                         span_open, sent[wsh: wsh + wlen], '</span>',
                         sent[wsh+wlen:]))
            )
        values.append((inst.id, loc_info, location))
    return ('id', 'location info', 'review'), values
