from django import forms
from django.core.validators import EmailValidator, RegexValidator

from . import widgets
from ..utils import dict_merge
from ..settings import error_messages, translated_error_messages


validate_name = RegexValidator(r'^([А-Яа-я]{1,50}|[A-Za-z]{1,50})$', message=error_messages['name'], code='invalid')
validate_login = RegexValidator(r'^[\w\-.@+]{4,50}$', message=error_messages['login'], code='invalid')
validate_password = RegexValidator(r'^.{6,50}$', message=error_messages['password'], code='invalid')


class Name(forms.CharField):
    widget = widgets.Name
    default_validators = [validate_name]

    def __init__(self, data_type='name', cell_size=1, **kwargs):
        self.cell_size = cell_size
        self.data_type = data_type
        kwargs = dict_merge(kwargs, {'error_messages': translated_error_messages})
        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['cell_size'] = self.cell_size
        attrs['data-type'] = self.data_type
        attrs['label'] = getattr(self, 'label', None)
        return attrs


class Email(forms.CharField):
    widget = widgets.Email
    default_validators = [EmailValidator(error_messages['email'])]

    def __init__(self, data_type='email', cell_size=1, **kwargs):
        self.cell_size = cell_size
        self.data_type = data_type
        kwargs = dict_merge(kwargs, {'error_messages': translated_error_messages})
        super().__init__(strip=True, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['cell_size'] = self.cell_size
        attrs['data-type'] = self.data_type
        attrs['label'] = getattr(self, 'label', None)
        return attrs


class Login(forms.CharField):
    widget = widgets.Login
    default_validators = [validate_login]

    def __init__(self, data_type='login', cell_size=1, **kwargs):
        self.cell_size = cell_size
        self.data_type = data_type
        kwargs = dict_merge(kwargs, {'error_messages': translated_error_messages})
        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['cell_size'] = self.cell_size
        attrs['data-type'] = self.data_type
        attrs['label'] = getattr(self, 'label', None)
        return attrs


class Password(forms.CharField):
    widget = widgets.Password  # EmailInput
    default_validators = [validate_password]

    def __init__(self, data_type='password', cell_size=1, **kwargs):
        self.cell_size = cell_size
        self.data_type = data_type
        kwargs = dict_merge(kwargs, {'error_messages': translated_error_messages})
        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['cell_size'] = self.cell_size
        attrs['data-type'] = self.data_type
        attrs['label'] = getattr(self, 'label', None)
        return attrs
