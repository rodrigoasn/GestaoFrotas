# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from .models import SystemConfiguration


# ────────────────────────────────────────────────────────────────────
# SESSÃO EXPIRADA
# ────────────────────────────────────────────────────────────────────
def session_expiry(request):
    if request.user.is_authenticated:
        return {
            'session_expiry_age': request.session.get_expiry_age(),
        }
    return {}


# ────────────────────────────────────────────────────────────────────
# SYSTEM CONFIGURATION
# ────────────────────────────────────────────────────────────────────
def system_configuration(request):
    return {
        'system_configuration': SystemConfiguration.objects.first()
    }
