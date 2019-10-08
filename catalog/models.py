from django.utils.timezone import now as current_time
from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from accounts.utils import dummy_deleted_user, default_user

from .settings import *


get_sentinel_user = dummy_deleted_user  # TODO: remove this shit after you done with temp
get_empty_user = default_user  # TODO: remove this shit after you done with temp

book_fs = FileSystemStorage(location=APP_PATH + '/books/')


class BaseWithMetaInfo(models.Model):
    inserter = models.ForeignKey(get_user_model(), on_delete=models.SET(dummy_deleted_user), default=default_user,
                                 related_name='added_%(class)ss',
                                 related_query_name='%(class)ss')
    date_joined = models.DateTimeField(default=current_time)
    checked = models.BooleanField(default=False)
    
    who_checked = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=default_user,
                                    related_name='checked_%(class)ss',
                                    related_query_name='%(class)ss_checked')
    date_checked = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_inserter_info(self):
        inserter = get_user_model().objects.get(id=self.inserter_id)
        adding_time = self.date_joined.replace(tzinfo=None).isoformat(sep='/', timespec='seconds')
        return 'inserted by `{}` at {} '.format(inserter, adding_time)

    def get_checking_info(self):
        reviever = get_user_model().objects.get(id=self.who_checked_id)
        accepting_time = self.date_checked.replace(tzinfo=None).isoformat(sep='/', timespec='seconds')
        return 'accepted by `{}` at {} '.format(reviever, accepting_time)


class Genre(BaseWithMetaInfo):
    name = models.CharField(
        max_length=GENRE_NAME_LEN,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        return self.name


class Language(BaseWithMetaInfo):
    name = models.CharField(
        max_length=LANG_NAME_LEN,
        help_text="Enter the book's natural language (e.g. Russian, English, French etc.)"
    )

    def __str__(self):
        return self.name


class Author(BaseWithMetaInfo):
    first_name = models.CharField(max_length=AUTHOR_FST_NAME_LEN)
    last_name = models.CharField(max_length=AUTHOR_LST_NAME_LEN)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)


class Book(BaseWithMetaInfo):
    title = models.CharField(max_length=BOOK_TITLE_LEN)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=SUMMARY_LEN, help_text="Enter a brief description of the book")
    file = models.FileField(storage=book_fs,
                            validators=[FileExtensionValidator(BOOK_EXTENSIONS)],
                            help_text="Upload your text of book in one single file here")
    isbn = models.CharField(
        'ISBN',
        max_length=ISBN_LEN,
        null=True,
        help_text='{} length character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
                  .format(ISBN_LEN)
    )

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    def __str__(self):
        return self.title


class Symbol(BaseWithMetaInfo):
    occurs_in = models.ManyToManyField(Book, through='Existence', through_fields=('symbol', 'book'))
    name = models.CharField(max_length=SYMBOL_NAME_LEN)

    def __str__(self):
        return self.name


class Existence(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,
                               related_name='existences',
                               related_query_name='exists')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='existence_set',
                             related_query_name='ex_set')

    class Meta:
        unique_together = ('symbol', 'book')

    def __str__(self):
        return '"{}" -> "{}"'.format(self.symbol, self.book)


class Location(BaseWithMetaInfo):
    existence = models.ForeignKey(Existence, on_delete=models.CASCADE,
                                  related_name='locations',
                                  related_query_name='located')
    start = models.PositiveIntegerField(help_text="Start of entry from file beginnings")
    word_shift = models.PositiveSmallIntegerField(help_text="Shift to Symbol existence from entry start address")
    word_len = models.PositiveSmallIntegerField(help_text="Length of Symbol (or his synonym) inside context")
    end_shift = models.PositiveSmallIntegerField(help_text="Shift to end of entry from start address")
    contexts = models.ManyToManyField('Context')

    class Meta:
        ordering = ['start', 'word_shift', 'word_len']

    def __str__(self):
        return '"{}" in "{}" from pos №{} with {} contexts'.format(
                   self.existence.symbol.name, self.existence.book.title, self.start, self.contexts.count()
        )

    def clean(self):
        if self.word_shift + self.word_len > self.end_shift:
            raise ValidationError("Symbol goes outside the existence boards!")


class ContextType(BaseWithMetaInfo):
    name = models.CharField(max_length=CONTEXT_TYPE_NAME_LEN)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Context(BaseWithMetaInfo):
    type = models.ForeignKey(ContextType, on_delete=models.CASCADE)
    text = models.CharField(max_length=CONTEXT_TEXT_LEN)

    class Meta:
        ordering = ['text']

    def __str__(self):
        return '[{}] {}'.format(self.type.name, self.text)
