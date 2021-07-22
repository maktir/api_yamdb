from django.db import models
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

ROLE_CHOICES = (
        ('user', 'user',),
        ('moderator', 'moderator',),
        ('admin', 'admin',),
    )


class User(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=ROLE_CHOICES,
                            default=ROLE_CHOICES[0][0],
                            max_length=30,
                            null=True,
                            blank=True)
    password = models.CharField(_('confirmation_code'), max_length=250)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return f'{self.username}'
