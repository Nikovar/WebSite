from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_up/ajax/', views.sign_up_ajax, name='sign_up_ajax'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_in/ajax', views.sign_in_ajax, name='sign_in_ajax'),
    path('sign_out', views.sign_out, name='sign_out'),
]
