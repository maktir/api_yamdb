from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=False)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.TextField()
    year = models.DateTimeField(
        "Дата издания",
        blank=True,
        null=True
    )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 blank=True,
                                 null=True,
                                 verbose_name='Категория',
                                 help_text='Тип произведения')
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              related_name='titles',
                              blank=True,
                              null=True,
                              verbose_name='Жанр',
                              help_text='Жанр произведения')

    def __str__(self):
        return self.name
