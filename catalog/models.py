from django.utils.timezone import now as current_time
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns... @gronix: let this existing for now
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from .settings import *

book_fs = FileSystemStorage(location=APP_PATH + '/books/')


class Genre(models.Model):
    name = models.CharField(
        max_length=GENRE_NAME_LEN,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=LANG_NAME_LEN,  # @gronix: i tried to find more longer name of language then this limit aaaand... i couldn't :D
        help_text="Enter the book's natural language (e.g. Russian, English, French etc.)"
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=AUTHOR_FST_NAME_LEN)
    last_name = models.CharField(max_length=AUTHOR_LST_NAME_LEN)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']


class Book(models.Model):
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
        help_text='{} Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'.format(ISBN_LEN)
    )

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class Symbol(models.Model):
    occurs_in = models.ManyToManyField(Book, through='Existence', through_fields=('symbol', 'book'))
    name = models.CharField(max_length=SYMBOL_NAME_LEN)

    def __str__(self):
        return self.name


class SymbolDescription(models.Model):
    text = models.TextField(max_length=SYMBOL_DESCRIPTION_LEN)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='descriptions')

    def __str__(self):
        return self.text if len(self.text) <= 20 else '{}...'.format(self.text[:17])


# this one only for the correct listing of symbol occurrences, which owner has left @gronix
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


# Standard Django's implementation for many-to-many relation with extra fields @gronix
class Existence(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,
                               related_name='existences',
                               related_query_name='exists')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='existence_set',
                             related_query_name='ex_set')
    inserter = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user),
                                 related_name='inserted',
                                 related_query_name='insert')
    date_joined = models.DateTimeField(default=current_time)

    def __str__(self):
        time = self.date_joined.isoformat(sep='/', timespec='seconds')
        return '"{}" -> "{}" (by {} at {})'.format(self.symbol, self.book, self.inserter, time)


# DISCLAIMER: All that is written below is subject to discussion. ;). @gronix
class Location(models.Model):
    existence = models.ForeignKey(Existence, on_delete=models.CASCADE,
                                  related_name='locations',
                                  related_query_name='located')
    start = models.PositiveIntegerField(help_text="Start of entry from file beginnings")
    word_shift = models.PositiveSmallIntegerField(help_text="Shift to Symbol existence from entry start address")
    word_len = models.PositiveSmallIntegerField(help_text="Length of Symbol (or his synonym) inside context")
    end_shift = models.PositiveSmallIntegerField(help_text="Shift to end of entry from start address")

    # @gronix:
    #   Django has stupid logics for model validation - framework docs suggests using
    #   forms based on models for validate model data (i.e. fields validations to
    #   compatibility with each other), aaand no another! (clear()/full_clear()/validate_unique()
    #   are not suitable for this - see docs)
    #   I think this kind of shi... They declared support for something more suitable only in version 2.2...

    #   So, I insist to use following approach for handling logically corrupt data.
    #   Because this is more general and will check data before storing in db for all cases
    #   (whether saving via views, django shell etc.)
    def save(self, *args, **kwargs):
        # @gronix: "try..except" may seem excessive, but i prefer to keep this code due to future structure
        #   corrections and for more general approach at the very beginnings of project.
        try:
            if self.word_shift + self.word_len > self.end_shift:
                raise ValidationError("Symbol goes outside the existence boards!")
        except ValidationError as e:
            print("ERROR! While saving was detected following:\n{}\nSaving aborted.\n".format(e.message))
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        sword_pos = self.start + self.word_shift
        eword_pos = sword_pos + self.word_len
        end = self.start + self.end_shift
        return '{} ({} - [{}..{}] - {}): {}'.format(self.existence.book.title,
                                                    self.start,
                                                    sword_pos,
                                                    eword_pos,
                                                    end,
                                                    self.existence.symbol.name)
