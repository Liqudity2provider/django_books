import asyncio
import concurrent.futures
import json
from itertools import islice

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

    def get(self, request, *args, **kwargs):
        """:return Books"""

        api_response = requests.get(
            PATH + 'books/api/',
            headers=self.headers,
            data=request.data,
        )
        output = api_response.json()

        context = {
            'books': output['results'],
        }
        return render(request, 'home.html', context)


class BookSearchView(ListView):
    model = Book

    def get(self, request, **kwargs):
        return render(request, 'books/search.html')

    def post(self, request):
        search_string = json.loads(request.body).get('searchText')

        books = Book.objects.annotate(count_of_reviews=Count('reviews')).order_by('-count_of_reviews').filter(
            name__icontains=search_string
        )

        data = list(books.values())

        for book in data:
            book.update({'link': f'../book/{book.get("id")}/'})

        return JsonResponse(data, safe=False)


class BookDetailView(APIView):

    def get(self, request, pk, **kwargs):
        """:return Book"""

        api_response = requests.get(
            PATH + 'book/api/' + str(pk),
            headers=self.headers,
            data={}
        )

        output = api_response.json()

        context = {
            'book': output,
        }
        return render(request, 'books/book_detail.html', context)


class ReviewDetailView(APIView):

    def get(self, request, pk, **kwargs):
        """:return Review"""

        review = Review.objects.get(pk=pk)
        comments = review.comments.select_related()

        context = {
            'review': review,
            'comments': comments,
            'comment_form': NewCommentForm(),
        }
        return render(request, 'books/review_detail.html', context)

    def post(self, request, pk):
        """adds new comment to Review"""

        review = Review.objects.get(pk=pk)
        comment_form = NewCommentForm(request.POST)

        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.review = Review.objects.get(pk=pk)
            user_comment.author = request.jwt_user
            user_comment.save()

            comment_form = NewCommentForm()

            context = {
                'review': review,
                'comments': review.comments.all(),
                'comment_form': comment_form,
            }
            return render(request, 'books/review_detail.html', context)


class BookCreateView(APIView):
    model = Book
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        response = Response(
            template_name='books/create_book.html', data={
                "form": BookForm()
            }
        )
        return response

    def post(self, request, *args, **kwargs):
        form_data = request.data

        requests.post(
            PATH + 'books/api/',
            headers=self.headers,
            data=form_data,
        )

        return redirect('books_main')


class BookDeleteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, *args, **kwargs):
        response = Response(
            template_name='books/book_delete.html', data={
                "book": Book.objects.get(pk=pk),
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

        response = Response(
            template_name='books/review_create.html', data={
                "form": ReviewForm(),
            }
        )

        return response

    def post(self, request, *args, **kwargs):

        form_data = dict(request.data)
        form_data.update({'user_id': request.jwt_user.pk, 'book_id': kwargs.get('pk')})

        requests.post(
            PATH + 'reviews/api/',
            headers=self.headers,
            data=form_data,
        )

        messages.success(request, 'Review created')
        return redirect('book_detail', kwargs.get('pk'))


class AuthorSearchView(ListView):
    model = Author

    def get(self, request, **kwargs):

        return render(request, 'books/search_authors.html', {'user': request.jwt_user})

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


def save_boooook(name):
    Book.objects.create(name=str(name), author_id=1)
    print(f'created {name}')


class AddBooks(ListView):

    def get(self, *args, **kwargs):
        batch_size = 100
        objs = (Book(name='Test %s' % i, author_id=1) for i in range(5000, 50000))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            b = Book.objects.bulk_create(batch, batch_size)
            # print(b.name)

        # names = [str(num) for num in range(1000, 2000)]
        # pool = Pool(processes=5)  # Create a multiprocessing Pool
        # pool.map(save_boooook, names)  # process data_inputs iterable with pool

        # auth = Author.objects.create(name='name')
        # for num in range(251, 1000):
        #     Book.objects.create(name=str(num), author_id=1)
        #     print(f'created {num}')
        return JsonResponse({})
