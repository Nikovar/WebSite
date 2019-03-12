from django.contrib import admin
from .models import Pack, Symbol, Addresses

# Register your models here.

admin.site.register(Pack)
admin.site.register(Symbol)
admin.site.register(Addresses)