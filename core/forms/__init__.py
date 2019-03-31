from django.core.exceptions import ObjectDoesNotExist
from django import forms

from catalog.models import Author

from . import fields
from ..settings import complex_error_messages


class BookChoosing(forms.Form):
    author = forms.ModelChoiceField(Author.objects.all(), empty_label="Выберите автора")
    book = fields.DynamicChoiceField(widget=forms.Select(attrs={'class': 'disabled', 'disabled': 'true'}),
                                                         choices=(('-1', ''),))

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        author = cleaned_data.get('author')
        try:
            author.book_set.get(id=int(book))
        except ObjectDoesNotExist:
            raise forms.ValidationError(message=complex_error_messages['author_book'], code="invalid")


class Registration(forms.Form):
    login = fields.Login(label="Логин", max_length=50, min_length=4)
    email = fields.Email(label='Почтовый адрес', max_length=100, cell_size=2)
    first_name = fields.Name(label='Имя', max_length=50)
    last_name = fields.Name(label='Фамилия', max_length=50)
    middle_name = fields.Name(label='Отчество', max_length=50, required=False)
    password = fields.Password(label='Пароль', max_length=50, min_length=6)
    password_repeat = fields.Password(label='Повторите пароль', max_length=50, min_length=6)

    layout = [(1, 2),
              (3, 4, 5),
              (6, 7, -1)]
    bindings = {1: 'login', 2: 'email', 3: 'first_name', 4: 'last_name', 5: 'middle_name', 6: 'password',
                7: 'password_repeat'}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError(message=complex_error_messages['pass_identity'], code="")


class Login(forms.Form):
    login = fields.Login(label="Логин", max_length=50, min_length=4, cell_size=1.5)
    password = fields.Password(label='Пароль', max_length=50, min_length=6, cell_size=1.5)

    layout = [(1, 2)]
    bindings = {1: 'login', 2: 'password'}
