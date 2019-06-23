"""
    Utilities for make manual migration of accepted model instances (via special admin interface).
"""

# importing constants and get access to important import of models:
from . import *


CLEANER_CHECKERS = {
    get_user_model()._meta.object_name: lambda user: not user.inserted.exists(),
    Location._meta.object_name: lambda loc: False,  # because of it never to be
    Existence._meta.object_name: lambda ex: not ex.locations.exists(),
    Symbol._meta.object_name: lambda symb: not symb.existences.exists(),
    # SymbolDescription._meta.object_name: lambda descr: False,  # because of CASCADE deleting descriptions of removed symbol
    Book._meta.object_name: lambda book: not book.existence_set.exists(),
    Language._meta.object_name: lambda lang: not lang.book_set.exists(),
    Genre._meta.object_name: lambda genre: not genre.book_set.exists(),
    Author._meta.object_name: lambda author: not author.book_set.exists(),
}


def genre_saver(tmp_genre, auto_saved_objects):
    # TODO: check whether this correct link related books when created new genre instance...
    return Genre.objects.get_or_create(name=tmp_genre.name)


def language_saver(tmp_language, auto_saved_objects):
    return Language.objects.get_or_create(name=tmp_language.name)


def author_saver(tmp_author, auto_saved_objects):
    is_new_author = False
    if Author.objects.filter(pk=tmp_author.pk,
                             first_name=tmp_author.first_name,
                             last_name=tmp_author.last_name)\
                     .exists():
        author = Author.objects.get(pk=tmp_author.pk)
    else:
        is_new_author = True
        author = Author.objects.create(first_name=tmp_author.first_name,
                                       last_name=tmp_author.last_name,
                                       date_of_birth=tmp_author.date_of_birth,
                                       date_of_death=tmp_author.date_of_death)
    return author, is_new_author


def book_saver(tmp_book, auto_saved_objects):
    is_new_book = False
    if tmp_book.file == '' and Book.objects.filter(pk=tmp_book.pk, title=tmp_book.title).exists():
        book = Book.objects.get(pk=tmp_book.pk)
    else:
        language = language_saver(tmp_book.language, auto_saved_objects)
        auto_saved_objects.append(tmp_book.language)

        author = author_saver(tmp_book.author, auto_saved_objects)
        auto_saved_objects.append(tmp_book.author)
        # TODO: check whether book will removed after delete temporary Book instance. (Should not)
        book = Book.objects.create(title=tmp_book.title,
                                   author=author,
                                   language=language,
                                   summary=tmp_book.summary,
                                   file=tmp_book.file,
                                   isbn=tmp_book.isbn)
        for single_genre in tmp_book.genre.all():
            g = genre_saver(single_genre, auto_saved_objects)
            auto_saved_objects.append(single_genre)

            book.genre.add(g)
        is_new_book = True
    return book, is_new_book


def symbol_saver(tmp_symbol, auto_saved_objects):
    symbol, is_new_symbol = Symbol.objects.get_or_create(name=tmp_symbol.name)
    for descr in tmp_symbol.descriptions.all():
        symbol_descr_saver(descr, auto_saved_objects, symbol)
        auto_saved_objects.append(descr)
    return symbol, is_new_symbol


def symbol_descr_saver(tmp_descr, auto_saved_objects, related_symbol=None):
    if related_symbol is None:
        related_symbol, _ = Symbol.objects.get_or_create(name=tmp_descr.symbol.name)
    # return SymbolDescription.objects.get_or_create(symbol=related_symbol, text=tmp_descr.text)
    return None


def location_saver(loc, auto_saved_objects):
    is_new_location = True

    book, is_new_book = book_saver(loc.existence.book, auto_saved_objects)
    auto_saved_objects.append(loc.existence.book)

    symbol, is_new_symbol = symbol_saver(loc.existence.symbol, auto_saved_objects)
    auto_saved_objects.append(loc.existence.symbol)

    existence, _ = Existence.objects.get_or_create(symbol=symbol, book=book)
    auto_saved_objects.append(loc.existence)

    inserter, _ = get_user_model().objects.get_or_create(username=loc.inserter.username)
    auto_saved_objects.append(loc.inserter)

    if not(is_new_book or is_new_symbol) \
        and Location.objects.filter(existence__book=book, existence__symbol=symbol,
                                    start=loc.start, word_shift=loc.word_shift,
                                    word_len=loc.word_len, end_shift=loc.end_shift).exists():
        location = Location.objects.get(existence__book=book, existence__symbol=symbol,
                                        start=loc.start, word_shift=loc.word_shift,
                                        word_len=loc.word_len, end_shift=loc.end_shift)
        is_new_location = False
    else:
        location = Location.objects.create(existence=existence,
                                           start=loc.start, word_shift=loc.word_shift,
                                           word_len=loc.word_len, end_shift=loc.end_shift,
                                           inserter=inserter)
    return location, is_new_location


def smart_cleaner(saving_track):
    for saved_obj in reversed(saving_track):
        if CLEANER_CHECKERS[saved_obj._meta.object_name](saved_obj):
            saved_obj.delete()
        # note: this will work properly because of `reversed` function:
        saving_track.remove(saved_obj)

