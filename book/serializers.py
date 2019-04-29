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
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer(many=False)

    class Meta:
        model = models.Book
        fields = ('title', 'authors', 'publisher', 'publication_date')

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')

        book = models.Book.objects.create(**validated_data)

        for author in authors_data:
            author, created = models.Author.objects.get_or_create(first_name=author['first_name'])
            book.authors.add(author)
        return book
