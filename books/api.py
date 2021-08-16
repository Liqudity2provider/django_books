from django.db.models import Count
from rest_framework import generics, status

from books.filter import CustomOrderFilter
from books.models import Book, Review, Author
from books.serializers import BookSerializer, ReviewSerializer
from rest_framework.response import Response


class BookApiListView(generics.ListCreateAPIView):
    """
    List or create books
    """

    serializer_class = BookSerializer
    queryset = Book.objects.annotate(count_of_reviews=Count('reviews')).order_by('-count_of_reviews')

    def create(self, request, *args, **kwargs):
        data = request.data
        self.perform_create(data)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, data):
        author = Author.objects.get(pk=data.get('author'))
        new_book = Book.objects.create(name=data.get('name'), author=author)
        new_book.save()


class BookApiDetailView(generics.RetrieveDestroyAPIView):
    """
    GET or DELETE Book by id
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()


class ReviewApiDetailView(generics.RetrieveAPIView):
    """
    Review by id
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewApiListView(generics.CreateAPIView):
    """
    Create Reviews
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        self.perform_create(data)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, data):
        new_review = Review.objects.create(
            title=data.get('title'),
            content=data.get('content'),
            review_author_id=data.get('user_id'),
            book_id=data.get('book_id')
        )
        new_review.save()
