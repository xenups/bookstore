from django.shortcuts import render
# Function Base View Tutorial
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from bookFBV.models import Book
from bookFBV.serializers import BookSerializer


class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({"books": serializer.data})

    def post(self, request):
        book = request.data.get('Book')
        serializer = BookSerializer(data=book)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()

        return Response({"succeeded" + book_saved.title})
