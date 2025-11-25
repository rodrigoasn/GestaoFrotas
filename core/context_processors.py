# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.conf import settings


# ────────────────────────────────────────────────────────────────────
# SESSION EXPIRY
# ────────────────────────────────────────────────────────────────────
def session_expiry(request):
    if request.user.is_authenticated:
        return {
            'session_expiry_age': request.session.get_expiry_age(),
        }
    return {}
