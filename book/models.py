from __future__ import unicode_literals
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=True)
    bio = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to="media", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=60, null=True)
    state_province = models.CharField(max_length=60, null=True)
    website = models.URLField(null=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Book(models.Model):
    title = models.CharField(max_length=50, verbose_name="موضوع")
    authors = models.ManyToManyField(Author, verbose_name="نویسنده")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ناشر")
    publication_date = models.DateField(blank=True, null=True, verbose_name="تاریخ انتشار")

    def __str__(self):
        return self.title
