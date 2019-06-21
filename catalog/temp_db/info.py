from collections import namedtuple

from . import *
from .data_formers import *
from .migrate_to_main import *


changes_render_binds = namedtuple('ChangesList', ['model_name', 'fields', 'values'])
model_binds = namedtuple('ModelInfo', ['name', 'model', 'get_render_data', 'saver'])


TRACKED_MODELS = (
    model_binds(Author._meta.object_name, Author, author_render_data, author_saver),
    model_binds(Book._meta.object_name, Book, book_render_data, book_saver),
    model_binds(Symbol._meta.object_name, Symbol, symbol_render_data, symbol_saver),
    # model_binds(SymbolDescription._meta.object_name, SymbolDescription, symbol_descr_render_data, symbol_descr_saver),
    model_binds(Location._meta.object_name, Location, location_render_data, location_saver)
)


def check_for_changes():
    return True if sum(smart_counter(m.model) for m in TRACKED_MODELS) > 0 else False


def get_not_accepted_data():
    changes = list(changes_render_binds(m.name, *m.get_render_data(m.model)) for m in TRACKED_MODELS)
    return changes


def smart_counter(model):
    m_manager = model.objects.using('temp')
    if model == Author:
        query = m_manager.exclude(date_of_birth=None, date_of_death=None)
    elif model == Book:
        query = m_manager.exclude(file='')
    elif model == Symbol:
        existed_symbols = set(Symbol.objects.values_list('name', flat=True))
        query = m_manager.exclude(name__in=existed_symbols)
    else:
        query = m_manager
    return query.count()
