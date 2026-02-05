# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.urls import path
from .views import SettingsView, ServiceWorkerView


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
    path('service-worker.js', ServiceWorkerView.as_view(), name='service_worker'),
]
