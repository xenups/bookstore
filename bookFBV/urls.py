from django.urls import path
from rest_framework import urlpatterns

from bookFBV.views import BookListView, BookDetailsView

urlpatterns = [
    path('books/<int:pk>', BookDetailsView.as_view({'get': 'retrieve'})),
    path('books/', BookListView.as_view()),

]
