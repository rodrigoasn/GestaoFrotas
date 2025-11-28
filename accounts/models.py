# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


# ────────────────────────────────────────────────────────────────────
# MODEL: CUSTOM USER
# ────────────────────────────────────────────────────────────────────
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('endereço de email'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
