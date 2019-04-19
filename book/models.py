from __future__ import unicode_literals

from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=60)
    website = models.URLField()

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
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, verbose_name="ناشر")
    publication_date = models.DateField(blank=True, null=True, verbose_name="تاریخ انتشار")

    def __str__(self):
        return self.title
