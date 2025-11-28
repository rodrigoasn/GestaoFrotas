# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# CUSTOM USER MANAGER
# ────────────────────────────────────────────────────────────────────
class CustomUserManager(BaseUserManager):
    """
    Gerenciador de usuário personalizado onde o email é o identificador único
    para autenticação em vez de nomes de usuário.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError(_('O email deve ser informado'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Cria e salva um SuperUser com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser tem que ter is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser tem que ter is_superuser=True'))
        return self.create_user(email, password, **extra_fields)
