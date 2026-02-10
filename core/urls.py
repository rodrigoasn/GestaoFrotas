# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.urls import path
from .views import SettingsView, ServiceWorkerView, CNPJSearchView, CEPSearchView


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
    path('service-worker.js', ServiceWorkerView.as_view(), name='service_worker'),
    path('api/cnpj/<str:cnpj>/', CNPJSearchView.as_view(), name='api_cnpj_search'),
    path('api/cep/<str:cep>/', CEPSearchView.as_view(), name='api_cep_search'),
]
