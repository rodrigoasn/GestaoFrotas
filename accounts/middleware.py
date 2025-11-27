# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime


# ────────────────────────────────────────────────────────────────────
# SESSION TIMEOUT MIDDLEWARE
# ────────────────────────────────────────────────────────────────────
class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get global timeout from SystemConfiguration
            try:
                from core.models import SystemConfiguration
                config = SystemConfiguration.objects.first()
                timeout_minutes = config.session_timeout_minutes if config else 30
            except Exception:
                timeout_minutes = 30
            
            request.session.set_expiry(timeout_minutes * 60)
        
        response = self.get_response(request)
        return response
