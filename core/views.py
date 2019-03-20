from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.core.exceptions import ValidationError
from django.conf import settings as site_settings
from django.http import HttpResponse

from accounts.settings import CHECK_ERRORS
from .forms import RegForm, LoginForm
from .utils import error_packer


def main(request):
    return render(request, 'core/home.html')


# def reg(request):
#     # if we come here after redirect from specific url, then we store POST data and get redirected as GET query
#     # TODO: remove this hack when you realize user cabinet:
#     form_data = request.POST if request.method == 'POST' else request.session.get('_reg_form_data', False)
#     if form_data:
#         checked, form = reg_form_process(form_data)
#         if checked:
#             return redirect('/')
#     else:
#         form = RegForm()
#     return render(request, 'core/auth/reg.html', {'form': form})
#
#
# def reg_ajax(request):
#     # if we come here after redirect from specific url, then we store POST data and get redirected as GET query
#     # TODO: remove this hack when you realize user cabinet:
#     form_data = request.POST if request.method == 'POST' else request.session.get('_reg_form_data', False)
#     if form_data:
#         checked, form = reg_form_process(form_data)
#         if checked:
#             return HttpResponse("OK")
#         errors_list = error_packer(form.errors)
#         return HttpResponse('<br/>'.join(errors_list))
#     return HttpResponse("You need pass data for register.", status=403, content_type="text/plain")
#
#
# def login(request):
#     # if we come here after redirect from specific url, then we store POST data and get redirected as GET query
#     # TODO: remove this hack when you realize user cabinet:
#     form_data = request.POST if request.method == 'POST' else request.session.get('_auth_form_data', False)
#     if form_data:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['login']
#             password = form.cleaned_data['password']
#
#             # TODO: check whether it proper work when user is inactive, i.e. 'user.is_active = False'.
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 form.add_error(field=None, error=ValidationError(message=CHECK_ERRORS['auth'], code='auth_fail'))
#
#             if len(form.errors) == 0:
#                 django_login(request, user)
#                 return redirect('core:main')
#     else:
#         form = LoginForm()
#     return render(request, 'core/auth/login.html', {'form': form})
#
#
# def login_ajax(request):
#     # if we come here after redirect from specific url, then we store POST data and get redirected as GET query
#     # TODO: remove this hack when you realize user cabinet:
#     form_data = request.POST if request.method == 'POST' else request.session.get('_auth_form_data', False)
#     if form_data:
#         ckecked, form = auth_form_process(form_data)
#         if ckecked:
#             return HttpResponse('OK')
#         errors_list = error_packer(form.errors)
#         return HttpResponse('<br/>'.join(errors_list))
#     return HttpResponse("You need pass data for login.", status=403, content_type="text/plain")


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
            form = LoginForm() if atype == 'login' else RegForm()
        return render(request, 'core/auth/{}.html'.format(atype), {'form': form})


def reg_form_process(request_data):
    form = RegForm(request_data)
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
    form = LoginForm(request_data)
    if form.is_valid():
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']

        # TODO: check whether it proper work when user is inactive, i.e. 'user.is_active = False'.
        user = authenticate(username=username, password=password)
        if user is None:
            # i.e. if 'user == None' then auth backend cant authenticate current 'login - password' pair.
            form.add_error(field=None, error=ValidationError(message=CHECK_ERRORS['auth'], code='auth_fail'))

        if len(form.errors) == 0:
            django_login(request, user)
            return True, {}
    return False, form
