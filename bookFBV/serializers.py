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

        def create(self, validated_data):
            # first we pop or get the the type of the data we want
            publish_data = validated_data.pop('publisher')
            authors_data = validated_data.pop('authors')
            # then we create an object  of book to put created data into it
            book = Book.objects.create(**validated_data)
            # then we create an object by pop ed type and finally we put it into book then we save it
            publish, created = Publisher.objects.get_or_create(name=publish_data['name'])
            book.publisher = publish
            book.save()
            for author in authors_data:
                author, created = Author.objects.get_or_create(first_name=author['first_name'])
                book.authors.add(author)

            book.save()
            return book
