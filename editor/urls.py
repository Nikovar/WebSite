from django.urls import path
from . import views


app_name = 'editor'
urlpatterns = [
    path('', views.select_book, {'method': 'simple'}, name='select_book'),
    path('ajax/', views.select_book, {'method': 'ajax'}, name='select_book_ajax'),
    path('<int:book_id>/', views.main, name='main'),
    path('symbols', views.symbols, name='symbols'),
    path('<int:book_id>/get_page/<int:page>', views.get_page, name='get_page'),
    path('addresses/', views.locations, name='locations'),
    path('contexts/', views.contexts, name='contexts'),
    path('context_types/', views.context_types, name='context_types'),
    path('<int:book_id>/store_location/', views.store_location, name='store_location'),
    path('<int:book_id>/store_context/', views.store_context, name='store_context'),
]
