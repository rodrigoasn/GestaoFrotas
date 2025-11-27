# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DO APP GERAL
# ────────────────────────────────────────────────────────────────────
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = _('Contas')
