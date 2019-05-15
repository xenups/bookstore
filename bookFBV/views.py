from django.shortcuts import render
# Function Base View Tutorial
# Create your views here.
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from bookFBV.models import Book
from bookFBV.serializers import BookSerializer


class BookDetailsView(APIView):
    def get(self, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        serializer = BookSerializer(book)
        return Response({"books": serializer.data})


class BookListView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        book = request.data.get("books")
        serializer = BookSerializer(data=book)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()
        return Response({"succeeded" + book_saved.title})
