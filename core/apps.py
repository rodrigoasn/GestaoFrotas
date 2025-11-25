# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DO APP GERAL
# ────────────────────────────────────────────────────────────────────
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _('Core')
