from django.utils.timezone import now as current_time
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(
        max_length=200,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{}, {}'.format(self.last_name, self.first_name)


class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    # display_genre.short_description = 'Genre'  # нужно ли это? пока выпилил

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Symbol(models.Model):
    occurs_in = models.ManyToManyField(Book,
                                       through='Existences',
                                       through_fields=('symbol', 'book'))
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SymbolDescription(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='descr')
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


# this one only for the correct listing of symbol occurrences, which owner has left
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


# Standard Django's implementation for many-to-many relation with extra fields:
class Existences(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    inserter = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='user_added')
    date_joined = models.DateTimeField(default=current_time)

    def __str__(self):
        time = self.date_joined.isoformat(sep='/', timespec='seconds')
        return '{} -> {} (by {} at {})'.format(self.symbol, self.book, self.inserter, time)

# TODO: add <TEMPORARY> model for not yet approved symbols and existences. @gronix
