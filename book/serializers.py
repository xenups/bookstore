from django.contrib.auth.models import User, Group
from django.core import exceptions
from rest_framework import serializers
from book import models
from book.models import UserProfile
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        # user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.save()
        return user

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        instance.password = user.get('password')
        instance.email = user.get('email')
        instance.first_name = user.get('first_name')
        instance.last_name = user.get('last_name')
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'bio','avatar')

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        instance.user.first_name = user.get('first_name')
        instance.user.last_name = user.get('last_name')
        instance.user.set_password(user.get('password'))
        instance.user.email = user.get('email')
        # every instances entity must be saved before return
        instance.user.save()
        bio = validated_data.pop('bio')
        avatar = validated_data.pop('avatar')
        instance.avatar = avatar
        instance.bio = bio
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = UserProfile.objects.get_or_create(user=user, bio=validated_data.pop('bio'),
                                                             avatar=validated_data.pop('avatar'))
        profile.save()
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
