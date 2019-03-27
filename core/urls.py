from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.main, name='main'),
    path('reg/', views.auth_handler, {'method': 'normal', 'atype': 'reg'}, name='reg'),
    path('reg/ajax/', views.auth_handler, {'method': 'ajax', 'atype': 'reg'}, name='reg_ajax'),
    path('login/', views.auth_handler, {'method': 'normal', 'atype': 'login'}, name='login'),
    path('login/ajax/', views.auth_handler, {'method': 'ajax', 'atype': 'login'}, name='login_ajax'),
    path('authors', views.authors_list, name='authors_list'),
    path('authors/<int:author_id>/', views.author, name='author'),
]
