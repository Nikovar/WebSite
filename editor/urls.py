from django.urls import path
from . import views

app_name = 'editor'
urlpatterns = [
	path('', views.select, name='select'),
	path('<int:book_id>/', views.main, name='main'),
	path('symbols', views.symbols, name='symbols'),
	path('addresses', views.addresses, name='addresses'),
]

