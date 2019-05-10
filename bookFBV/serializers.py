# Function Base View Tutorial
from rest_auth.app_settings import serializers

from bookFBV.models import Book, Author, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'email')


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name', 'address', 'city', 'state_province', 'website')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publishers = PublisherSerializer(many=False)

    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher')
