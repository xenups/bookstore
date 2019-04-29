from django.shortcuts import render
from rest_framework import generics
from book import serializers
from book import models
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

# Create your views here.
from book.permissions import IsLoggedInUserOrAdmin, IsAuthenticatedNotPost


class BookList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    #   permission_classes = (IsAuthenticatedNotPost,)
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
