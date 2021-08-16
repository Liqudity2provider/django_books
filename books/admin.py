from django.contrib import admin
from .models import Author, Review, Book, Comment

admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Comment)

