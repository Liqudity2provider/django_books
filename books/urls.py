from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .api import BookApiListView, BookApiDetailView, ReviewApiDetailView, ReviewApiListView
from .views import BooksMainPage, BookSearchView, BookDetailView, ReviewDetailView, BookCreateView, BookDeleteView, \
    ReviewCreateView, AuthorSearchView

urlpatterns = [
    path('', BooksMainPage.as_view(), name='books_main'),
    path('books/api/', BookApiListView.as_view()),
    path('reviews/api/', ReviewApiListView.as_view()),
    path('search/', csrf_exempt(BookSearchView.as_view()), name="book_search"),
    path('search_authors/', csrf_exempt(AuthorSearchView.as_view()), name="author_search"),
    path('book/api/<int:pk>/', BookApiDetailView.as_view(), name='api_book_detail'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('review/api/<int:pk>/', ReviewApiDetailView.as_view(), name='api_review_detail'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('book/create/', BookCreateView.as_view(), name="book_create"),
    path('book/delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
    path('book/<int:pk>/review/create/', ReviewCreateView.as_view(), name="review_create"),
]
