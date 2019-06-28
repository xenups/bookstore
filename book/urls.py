from django.conf.urls import url
from rest_framework import routers

from book import views
from django.urls import path, include

from book.views import BookSearchView

router = routers.DefaultRouter()
# router.register("album/search", BookSearchView)
router.register(r'book/search/', BookSearchView, basename='Book')


urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('usersProfile/', views.UserProfileList.as_view()),
    path('usersProfile/<int:pk>/', views.UserProfileDetail.as_view()),
    # url(r'^api/', include(router.urls)),

]
