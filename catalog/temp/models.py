from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator

from ..settings import *  # import all db field limits
from ..models import current_time
# this will override 'APP_PATH' constant from catalog.settings,
# so behaviour is proper - will loaded APP_PATH for 'temp' app:
from .settings import *

book_fs = FileSystemStorage(location=APP_PATH + '/books/')


class Pack(models.Model):
    # explaining of choice for 'max_length' for author:
    #   all author info in temporary pack is stored into single string in format:
    #       "first_name<DELIM>last_name<DELIM>xx.xx.xxx<DELIM>yy.yy.yyyy",
    #   where xx.. = birth date, and yy.. = end date (i.e. date of death, if exist)
    author_info = models.CharField(max_length=AUTHOR_FST_NAME_LEN + AUTHOR_LST_NAME_LEN + DATE_STRING_REPR_LEN * 2 + DELIM_LEN * 3,
                                   help_text='Type by format: <first_name>{0}<last_name>{0}<bdate>{0}<edate>'.format(DELIM))
    book_title = models.CharField(max_length=BOOK_TITLE_LEN)
    book_genre = models.CharField(max_length=GENRE_NAME_LEN)
    book_file = models.FileField(storage=book_fs, validators=[FileExtensionValidator(BOOK_EXTENSIONS)])
    # in respective with following, 'book_extras' will contain book information in format:
    #       "language<DELIM>summary<DELIM>isbn"
    book_extras = models.TextField(max_length=LANG_NAME_LEN + SUMMARY_LEN + ISBN_LEN + DELIM_LEN * 2,
                                   help_text='Type by format: <language>{0}<summary>{0}<isbn>'.format(DELIM))

    inserter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='inserted_temp', related_query_name='ins_tmp')
    date_joined = models.DateTimeField(default=current_time)
    checked = models.NullBooleanField(default=None)

    def __str__(self):
        return self.book_title

    class Meta:
        ordering = ['book_title']


class TempSchema(models.Model):
    approved = models.NullBooleanField(default=None)

    class Meta:
        abstract = True


class Symbol(TempSchema):
    occurs_in = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='symbols', related_query_name='symb')
    name = models.CharField(max_length=SYMBOL_NAME_LEN)

    def __str__(self):
        return self.name


class Addresses(TempSchema):
    owner = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='addresses', related_query_name='adr')

    start = models.PositiveIntegerField()
    word_shift = models.PositiveSmallIntegerField()
    word_len = models.PositiveSmallIntegerField()
    end_shift = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
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
        return '({} - [{}..{}] - {})'.format(self.start, sword_pos, eword_pos, end)
