from django.contrib import admin

from .models import Author, Genre, Book, Language, Symbol, Existence, Location, ContextType, Context


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Symbol)
admin.site.register(Existence)
admin.site.register(Location)
admin.site.register(ContextType)
admin.site.register(Context)
