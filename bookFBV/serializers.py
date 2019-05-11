# Function Base View Tutorial
from rest_framework import serializers

from bookFBV.models import Book, Author, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'email')

        def create(self, validate_data):
            return Author.objects.create(**validate_data)


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name', 'address', 'city', 'state_province', 'website')

        def create(self, validate_data):
            return Publisher.objects.create(**validate_data)


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer(many=False)

    class Meta:
        model = Book
        fields = ('title', 'authors', 'publisher', 'publication_date')

        def create(self, validate_data):
            return Book.objects.create(**validate_data)
