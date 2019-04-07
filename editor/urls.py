from django.urls import path
from . import views


app_name = 'editor'
urlpatterns = [
	path('', views.select, {'method': 'simple'}, name='select'),
	path('ajax/', views.select, {'method': 'ajax'}, name='select_ajax'),
	path('<int:book_id>/', views.main, name='main'),
	path('symbols', views.symbols, name='symbols'),
	path('<int:book_id>/get_page/<int:page>', views.get_page, name='get_page'),
	path('addresses/', views.addresses, name='addresses'),
]
