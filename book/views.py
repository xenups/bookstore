from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework.mixins import UpdateModelMixin

from book import serializers
from book import models
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

# Create your views here.
from book.models import UserProfile
from book.permissions import IsLoggedInUserOrAdmin, IsAuthenticatedNotPost


class BookList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    #   permission_classes = (IsAuthenticatedNotPost,)
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView, UpdateModelMixin):
    # queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        username = self.kwargs['pk']
        return UserProfile.objects.filter(user_id='23')
