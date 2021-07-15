from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата отзыва', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)],)
    

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review  = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, 
    )

    def __str__(self):
        return self.text
