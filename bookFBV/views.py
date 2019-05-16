from django.shortcuts import render
# Function Base View Tutorial
# Create your views here.
from rest_framework import generics, status
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
        for key in request.data:
            print(key)
        print(request.data["title"])
        a_book = Book.objects.create(title=request.data["title"],
                                     )

        return Response(
            BookSerializer(a_book).data,
            status=status.HTTP_201_CREATED
        )
