from django.contrib import admin

# Register your models here.
from bookFBV.models import Book, Author, Publisher

from django_jalali.admin.filters import JDateFieldListFilter

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    fields = ('title', 'authors', 'publisher', 'publication_date')
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)
    list_filter = (
        ('publication_date', JDateFieldListFilter),
    )


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)

# Function Base View Tutorial
