from django.contrib import admin

from .models import (Title, Category, Genre,
                     Comment, Review)

admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)