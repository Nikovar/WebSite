from django.urls import path

from django.views.generic import TemplateView  # <- TODO: remove this after creating new views
from . import views

# == @gronix: all views are meaningless, so they are need to be changed to something more useful ==

urlpatterns = [
    path('', TemplateView.as_view(template_name='closed.html'))
    # path('', views.index, name='index'),
    #
    # path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # path('books/', views.BookListView.as_view(), name='books'),
    #
    # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # # Add URLConf for librarian to renew a book.
    # path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    # # Add URLConf to create, update, and delete books
    # path('book/create/', views.BookCreate.as_view(), name='book_create'),
    # path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    # path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    #
    # path('authors/', views.AuthorListView.as_view(), name='authors'),
    #
    # path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    # # Add URLConf to create, update, and delete authors
    # path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    # path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    # path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    #
    # path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),  # Added for challenge
    # path('about', views.BookCreate.as_view(), name='book_create')
]
