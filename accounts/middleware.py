from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get user specific timeout or default to 30 minutes
            timeout_minutes = getattr(request.user, 'session_timeout_minutes', 30)
            request.session.set_expiry(timeout_minutes * 60)
        
        response = self.get_response(request)
        return response
