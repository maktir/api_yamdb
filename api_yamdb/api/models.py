from django.db import models
import datetime as dt


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название Жанра')
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название Категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(default=lambda: dt.date.today().year,
                               verbose_name='Категория',
                               blank=True,
                               null=True
                               )
    rating = models.DecimalField(verbose_name='Рейтинг',
                                 max_digits=2,
                                 decimal_places=2,
                                 blank=True,
                                 null=True
                                 )
    description = models.CharField(max_length=200,
                                   verbose_name='Описание',
                                   blank=True,
                                   null=True
                                   )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 blank=True,
                                 null=True,
                                 verbose_name='Категория',
                                 help_text='Тип произведения'
                                 )
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              related_name='titles',
                              blank=True,
                              null=True,
                              verbose_name='Жанр',
                              help_text='Жанр произведения')

    def __str__(self):
        return self.name
