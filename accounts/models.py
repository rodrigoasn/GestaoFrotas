from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    session_timeout_minutes = models.PositiveIntegerField(
        default=30,
        help_text=_("Tempo de inatividade em minutos antes de expirar a sessão.")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
