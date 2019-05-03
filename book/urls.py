from book import views
from django.urls import path

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('users/', views.UserList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    path('usersProfile/', views.UserProfileList.as_view()),
    path('usersProfile/<int:pk>/', views.UserProfileDetail.as_view()),

]
