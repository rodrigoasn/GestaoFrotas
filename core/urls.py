# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.urls import path
from .views import DashboardView, SettingsView, ServiceWorkerView, CNPJSearchView, CEPSearchView


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # Configurações
    path('settings/', SettingsView.as_view(), name='settings'),

    # Service Worker
    path('service-worker.js', ServiceWorkerView.as_view(), name='service_worker'),

    # APIs
    path('api/cnpj/<str:cnpj>/', CNPJSearchView.as_view(), name='api_cnpj_search'),
    path('api/cep/<str:cep>/', CEPSearchView.as_view(), name='api_cep_search'),
]
