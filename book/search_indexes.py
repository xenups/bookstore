from django.utils import timezone
from haystack import indexes
from .models import Book, Publisher, Author, UserProfile


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")
    authors = indexes.CharField(model_attr="authors")
    publisher = indexes.CharField(model_attr="publisher")

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=timezone.now())
