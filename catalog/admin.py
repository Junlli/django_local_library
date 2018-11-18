from django.contrib import admin
from .models import Book, BookInstance, Genre, Author, Language

# Register your models here.
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
# admin.site.register(Author)
admin.site.register(Language)


class BookInline(admin.TabularInline):
    model = Book


# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_summary')
    fields = ['name', 'author_summary']
    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ('title', 'author', 'genre')
    inlines = [BookInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
