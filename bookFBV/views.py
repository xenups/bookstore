from django.shortcuts import render
# Function Base View Tutorial
# Create your views here.
# This Class Base View
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from bookFBV.models import Book
from bookFBV.serializers import BookSerializer


class BookDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get(self, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        serializer = BookSerializer(book)
        return Response({"books": serializer.data})

    def put(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        serializer = BookSerializer()
        b_serialezer = serializer.update(book, request.data)
        return Response({"success": "Book  updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        book = get_object_or_404(Book.objects.all(), pk=self.kwargs['pk'])
        book.delete()
        return Response({"book deleted"}, status=status.HTTP_200_OK)


class BookListView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        a_book = Book.objects.create(title=request.data["title"], )

        return Response(
            BookSerializer(a_book).data,
            status=status.HTTP_201_CREATED
        )
