from django import forms


class Name(forms.TextInput):
    template_name = 'core/forms/widgets/reg/name.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widg = context['widget']
        widg['spread'] = widg['attrs'].pop('cell_size', 1)
        widg['label'] = widg['attrs'].pop('label', None)
        return context


class Login(forms.TextInput):
    template_name = 'core/forms/widgets/reg/login.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widg = context['widget']
        widg['spread'] = widg['attrs'].pop('cell_size', 1)
        widg['label'] = widg['attrs'].pop('label', None)
        return context


class Email(forms.EmailInput):
    input_type = 'email'
    template_name = 'core/forms/widgets/reg/email.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widg = context['widget']
        widg['spread'] = widg['attrs'].pop('cell_size', 1)
        widg['label'] = widg['attrs'].pop('label', None)
        return context


class Password(forms.PasswordInput):
    template_name = 'core/forms/widgets/reg/password.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widg = context['widget']
        widg['spread'] = widg['attrs'].pop('cell_size', 1)
        widg['label'] = widg['attrs'].pop('label', None)
        return context
