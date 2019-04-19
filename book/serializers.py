from rest_framework import serializers
from book import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('first_name', 'last_name', 'email')


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ('name', 'address', 'city', 'state_province', 'website')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    publisher = PublisherSerializer(read_only=True, many=False)

    class Meta:
        model = models.Book
        fields = ('title', 'authors', 'publisher', 'publication_date')
