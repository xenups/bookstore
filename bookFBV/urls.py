from django.urls import path
from rest_framework import urlpatterns

from bookFBV.views import BookView

urlpatterns = [
    path('books/', BookView.as_view()),
    path('books/<int:pk>', BookView.as_view())


]
