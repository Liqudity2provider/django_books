from rest_framework import serializers
from books.models import Book, Review, Comment, Author


class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'reviews')

    def get_reviews(self, instance):
        if isinstance(instance, dict):
            book = Book.objects.get(pk=instance.get('pk'))
        else:
            book = Book.objects.get(pk=instance.pk)

        return [{'id': review.pk,
                 'title': review.title,
                 'content': review.content,
                 'review_author': review.review_author.username
                 } for review in book.reviews.all()]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'content', 'review_author', 'book', 'comments')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'review',
            'author',
            'parent',
            'content',
            'publish',
            'status',
        ]
