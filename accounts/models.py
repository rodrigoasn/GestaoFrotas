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
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', null=True, blank=True, help_text=_("JPG ou PNG. Tamanho máximo de 1MB."))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
