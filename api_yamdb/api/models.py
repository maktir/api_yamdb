from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime as dt

User = get_user_model()


class Review(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        'Дата отзыва', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey('Title', on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField(default=10, validators=[MinValueValidator(0),
                                                        MaxValueValidator(10)], )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments', null=False, blank=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, )

    def __str__(self):
        return self.text


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        default=dt.date.today().year,
        verbose_name='Дата выхода',
        blank=True,
        null=True
    )
    rating = models.DecimalField(
        verbose_name='Рейтинг',
        max_digits=2,
        decimal_places=2,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Тип произведения'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Жанр',
        help_text='Жанр произведения'
    )

    def __str__(self):
        return self.name
