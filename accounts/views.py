from django.shortcuts import render, redirect


# TODO: change this to more general approach: user account profile (with separate template from base theme)
def sign_up(request):
    request.session['_reg_form_data'] = request.POST
    return redirect('core:reg')


def sign_up_ajax(request):
    request.session['_reg_form_data'] = request.POST
    return redirect('core:reg_ajax')


def sign_in(request):
    request.session['_login_form_data'] = request.POST
    return redirect('core:login')


def sign_in_ajax(request):
    request.session['_login_form_data'] = request.POST
    return redirect('core:login_ajax')
