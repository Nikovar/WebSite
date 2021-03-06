from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.core.exceptions import ValidationError
from django.conf import settings as site_settings
from django.http import HttpResponse

from accounts.settings import CHECK_ERRORS
from catalog.models import Author
from .forms import Registration, Login
from .utils import error_packer


def main(request):
    authors = Author.objects.all()[:4]
    return render(request, 'core/home.html', {'authors': authors})


def authors_list(request):
    authors = Author.objects.all()
    return render(request, 'core/authors_list.html', {'authors': authors})


def author(request, author_id):
    author_ = get_object_or_404(Author, id=author_id)
    return render(request, 'core/author.html', {'author': author_})


def auth_handler(request, method, atype):
    # if we come here after redirect from specific url, then we store POST data and get redirected as GET query
    # TODO: remove this hack when you realize user cabinet:
    form_data = request.POST if request.method == 'POST' else request.session.get('_{}_form_data'.format(atype), False)

    if method == 'ajax':
        if form_data:
            checked, form = login_form_process(form_data, request) if atype == 'login' else reg_form_process(form_data)
            if checked:
                return HttpResponse('OK')
            errors_list = error_packer(form.errors)
            return HttpResponse('<br/>'.join(errors_list))
        return HttpResponse("You need pass data for {}.".format(atype), status=403, content_type="text/plain")
    else:
        if form_data:
            checked, form = login_form_process(form_data, request) if atype == 'login' else reg_form_process(form_data)
            if checked:
                return redirect('/')
        else:
            form = Login() if atype == 'login' else Registration()
        return render(request, 'core/auth/{}.html'.format(atype), {'form': form})


def reg_form_process(request_data):
    form = Registration(request_data)
    if form.is_valid():
        data = form.cleaned_data
        data.pop('password_repeat')  # this one should exist, but dont needed

        user_manager = get_user_model().objects
        if user_manager.check_username_existence(data['login']):
            form.add_error(field=None, error=ValidationError(message=CHECK_ERRORS['user_exists'], code="user_exists"))
        if user_manager.check_email_taken(data['email']):
            form.add_error(field=None, error=ValidationError(CHECK_ERRORS['email_taken'], code="email_taken"))

        if len(form.errors) == 0:
            new_user = user_manager.create_user(username=data.pop('login'), **data)

            # sending user activation code to his email
            if site_settings.ENABLE_EMAIL_CONFIRMATION:
                pass
                # new_user.email_activation_code()  # TODO: realize this functionality
            return True, {}
    return False, form


def login_form_process(request_data, request):
    form = Login(request_data)
    if form.is_valid():
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            # i.e. if 'user == None' then auth backend cant authenticate current 'login - password' pair.
            form.add_error(field=None, error=ValidationError(message=CHECK_ERRORS['auth'], code='auth_fail'))

        if len(form.errors) == 0:
            django_login(request, user)
            return True, {}
    return False, form
