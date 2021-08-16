import json
from django.contrib import messages
import requests
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from books.forms import NewCommentForm, BookForm, ReviewForm
from books.models import Book, Review, Author
from django_books import settings
from users.utils import refresh_token_or_redirect, user_from_token

PATH = settings.URL_PATH


class BooksMainPage(APIView):

    def get(self, request, **kwargs):
        """:return Books"""

        token = refresh_token_or_redirect(request)

        api_response = requests.get(
            PATH + 'books/api/',
            headers=self.headers,
            data=request.data
        )

        output = api_response.json()

        context = {
            'books': output,
            'user': user_from_token(token),
        }
        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        ...


class BookSearchView(ListView):
    model = Book

    def get(self, request, **kwargs):
        token = refresh_token_or_redirect(request)

        return render(request, 'books/search.html', {'user': user_from_token(token)})

    def post(self, request):
        search_string = json.loads(request.body).get('searchText')
        books = Book.objects.annotate(count_of_reviews=Count('reviews')).order_by('-count_of_reviews').filter(
            name__icontains=search_string
            )
        data = list(books.values())
        res_data = []
        for book in data:
            book.update({'link': f'../book/{book.get("id")}/'})
            res_data.append(book)
        return JsonResponse(list(res_data), safe=False)


class BookDetailView(APIView):

    def get(self, request, pk, **kwargs):
        """:return Book"""

        token = refresh_token_or_redirect(request)

        api_response = requests.get(
            PATH + 'book/api/' + str(pk),
            headers=self.headers,
            data={}
        )

        output = api_response.json()

        context = {
            'book': output,
            'user': user_from_token(token),
        }
        return render(request, 'books/book_detail.html', context)

    def post(self, request, pk):
        """adds new review to Book"""
        # ToDo write method
        ...


class ReviewDetailView(APIView):

    def get(self, request, pk, **kwargs):
        """:return Review"""

        token = refresh_token_or_redirect(request)

        review = Review.objects.get(pk=pk)

        context = {
            'review': review,
            'comments': review.comments.all(),
            'comment_form': NewCommentForm(),
            'user': user_from_token(token),
        }
        return render(request, 'books/review_detail.html', context)

    def post(self, request, pk):
        """adds new comment to Review"""

        token = refresh_token_or_redirect(request)

        review = Review.objects.get(pk=pk)
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.review = Review.objects.get(pk=pk)
            user_comment.author = user_from_token(token)
            user_comment.save()

            comment_form = NewCommentForm()

            context = {
                'review': review,
                'comments': review.comments.all(),
                'comment_form': comment_form,
                'user': user_from_token(token)
            }
            return render(request, 'books/review_detail.html', context)


class BookCreateView(APIView):
    model = Book
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

        response = Response(
            template_name='books/create_book.html', data={
                "form": BookForm()
            }
        )
        response.set_cookie('token', token)
        return response

    def post(self, request, *args, **kwargs):
        form_data = request.data

        response = requests.post(
            PATH + 'books/api/',
            headers=self.headers,
            data=form_data,
        )

        return redirect('books_main')


class BookDeleteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, *args, **kwargs):
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

        response = Response(
            template_name='books/book_delete.html', data={
                "book": Book.objects.get(pk=pk),
                'user': user_from_token(token)
            }
        )
        return response

    def post(self, request, pk, *args, **kwargs):
        requests.delete(
            PATH + 'book/api/' + str(pk) + '/',
            headers=self.headers,
            data=json.dumps({'data': "None"})
        )
        return redirect('books_main')


class ReviewCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        token = refresh_token_or_redirect(request)

        if not isinstance(token, str):
            return redirect('logout')

        response = Response(
            template_name='books/review_create.html', data={
                "form": ReviewForm(),
                "user": user_from_token(token)
            }
        )

        return response

    def post(self, request, *args, **kwargs):
        token = refresh_token_or_redirect(request)

        form_data = dict(request.data)
        form_data.update({'user_id': user_from_token(token).pk, 'book_id': kwargs.get('pk')})
        print(form_data)
        response = requests.post(
            PATH + 'reviews/api/',
            headers=self.headers,
            data=form_data,
        )
        messages.success(request, 'Review created')
        return redirect('books_main')


class AuthorSearchView(ListView):
    model = Author

    def get(self, request, **kwargs):
        token = refresh_token_or_redirect(request)

        return render(request, 'books/search_authors.html', {'user': user_from_token(token)})

    def post(self, request):
        search_string = json.loads(request.body).get('searchText')
        authors = Author.objects.filter(
            name__icontains=search_string
            )
        data = list(authors.values())
        res_data = []
        for author in data:
            author.update({'link': f'../'})
            res_data.append(author)
        return JsonResponse(list(res_data), safe=False)
