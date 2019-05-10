from django.contrib import admin

# Register your models here.
from bookFBV.models import Book, Author, Publisher

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)

# Function Base View Tutorial
