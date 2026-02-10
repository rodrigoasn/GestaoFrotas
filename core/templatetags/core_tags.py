# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django import template
from core.models import SystemConfiguration


# ────────────────────────────────────────────────────────────────────
# REGISTROS DE TAGS
# ────────────────────────────────────────────────────────────────────
register = template.Library()


# ────────────────────────────────────────────────────────────────────
# TAGS
# ────────────────────────────────────────────────────────────────────
@register.simple_tag
def get_system_configuration():
    """
    Retorna a instância única de SystemConfiguration.
    Útil para templates de e-mail onde o context_processor não está disponível.
    """
    try:
        return SystemConfiguration.objects.first()
    except Exception:
        return None
