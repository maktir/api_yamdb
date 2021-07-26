from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [(USER, 'user'),
                    (MODERATOR, 'moderator'),
                    (ADMIN, 'admin'), ]


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=UserRole.ROLE_CHOICES,
                            default=UserRole.ROLE_CHOICES[0][0],
                            max_length=30,
                            null=True,
                            blank=True)
    password = models.CharField(_('confirmation_code'), max_length=250, editable=False)

    @property
    def is_admin(self):
        if self.role == UserRole.ROLE_CHOICES[2][0] or self.is_staff:
            return True

    @property
    def is_moderator(self):
        if self.role == UserRole.ROLE_CHOICES[1][0]:
            return True

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return f'{self.username}'
