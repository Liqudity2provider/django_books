from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination

from books.models import Book, Review, Author
from books.serializers import BookSerializer, ReviewSerializer, AuthorSerializer
from rest_framework.response import Response


class BookApiListView(generics.ListCreateAPIView):
    """
    List or create books
    """

    serializer_class = BookSerializer
    queryset = Book.objects.annotate(count_of_reviews=Count('reviews')).order_by('-count_of_reviews')
    pagination_class = LimitOffsetPagination

    def __init__(self, *args, **kwargs):
        """Define number of objects per page"""

        self.pagination_class.default_limit = 10
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        author_id = request.data.get('author')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.author_id = request.data.get('author')
        self.perform_create(serializer, author_id)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(author_id=args[0])


class BookApiDetailView(generics.RetrieveDestroyAPIView):
    """
    GET or DELETE Book by id
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_object(self):

        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {"pk": self.kwargs["pk"]}

        obj = get_object_or_404(queryset, **filter_kwargs)

        return obj


class ReviewApiDetailView(generics.RetrieveAPIView):
    """
    Review by id
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = LimitOffsetPagination

    def __init__(self, *args, **kwargs):
        """Define number of objects per page"""

        self.pagination_class.default_limit = 5
        super().__init__(*args, **kwargs)


class ReviewApiListView(generics.CreateAPIView):
    """
    Create Reviews
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = LimitOffsetPagination

    def __init__(self, *args, **kwargs):
        """Define number of objects per page"""

        self.pagination_class.default_limit = 5
        super().__init__(*args, **kwargs)

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


class AuthorApiListView(generics.ListCreateAPIView):
    """
    List or create authors
    """

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = LimitOffsetPagination

    def __init__(self, *args, **kwargs):
        """Define number of objects per page"""

        self.pagination_class.default_limit = 5
        super().__init__(*args, **kwargs)


class AuthorApiDetailView(generics.RetrieveDestroyAPIView):
    """
    GET or DELETE Author by id
    """

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = LimitOffsetPagination

    def __init__(self, *args, **kwargs):
        """Define number of objects per page"""

        self.pagination_class.default_limit = 5
        super().__init__(*args, **kwargs)
