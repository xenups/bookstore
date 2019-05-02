from django.contrib.auth.models import User, Group
from rest_framework import serializers
from book import models
from book.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'created_at', 'updated_at', 'bio',
        )
        read_only_fields = ('created_at', 'updated_at',)

    def update(self, instance, validated_data):
        # First, update the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        # Then, update UserProfile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)

        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


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

    def update(self, instance, validated_data):
        publish_data = validated_data.pop('publisher')
        authors_data = validated_data.pop('authors')
        # we fill instances with validated data
        instance.title = validated_data['title']
        instance.publication_date = validated_data['publication_date']
        # we fill nested serializer like we defined in create
        publish, created = models.Publisher.objects.get_or_create(name=publish_data['name'])
        instance.publisher = publish
        # we fill nested serializer like we defined in create
        # its multiple data form, we have multiple authors for a book
        authors_list = []
        for author in authors_data:
            author, created = models.Author.objects.get_or_create(first_name=author['first_name'])
            authors_list.append(author)

        instance.authors.set(authors_list)
        instance.save()
        return instance
