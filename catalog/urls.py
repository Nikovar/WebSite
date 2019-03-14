from django.urls import path

from django.views.generic import TemplateView  # <- TODO: remove this after creating new views
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='catalog/home.html'))
]
