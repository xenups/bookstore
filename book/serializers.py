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
        # first we pop or get the the type of the data we want
        publish_data = validated_data.pop('publisher')
        authors_data = validated_data.pop('authors')
        # then we create an object  of book to put created data into it
        book = models.Book.objects.create(**validated_data)
        # then we create an object by pop ed type and finally we put it into book then we save it
        publish, created = models.Publisher.objects.get_or_create(name=publish_data['name'])
        book.publisher = publish
        book.save()
        for author in authors_data:
            author, created = models.Author.objects.get_or_create(first_name=author['first_name'])
            book.authors.add(author)

        book.save()
        return book
