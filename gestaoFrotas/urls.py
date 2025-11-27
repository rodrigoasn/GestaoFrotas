# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.urls import path, include
from core.views import SettingsView
from django.conf.urls.i18n import i18n_patterns


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('accounts.urls')),
    path('settings/', SettingsView.as_view(), name='settings'),
)
