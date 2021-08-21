from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Author(models.Model):
    name = models.CharField(max_length=40)

    def __repr__(self):
        return self.name



class Book(models.Model):
    name = models.CharField(max_length=80)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Comment(MPTTModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return self.content
