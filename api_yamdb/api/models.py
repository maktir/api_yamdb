from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime as dt

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='жанр',
        unique=True,
        null=True,
        blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='категория',
        unique=True,
        null=True,
        blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        default=dt.date.today().year,
        verbose_name='Дата выхода',
        blank=True,
        null=True,
        db_index=True
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        blank=True, null=True, verbose_name='Категория'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Review(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        'Дата отзыва', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.PositiveSmallIntegerField(default=10,
                                             validators=[MinValueValidator
                                                         (1, 'Min value is 1'),
                                                         MaxValueValidator
                                                         (10, 'Max value is 10'
                                                          )],)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               null=False, blank=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, )

    def __str__(self):
        return f'{self.text}'

    class Meta:
        ordering = ['-pub_date']
