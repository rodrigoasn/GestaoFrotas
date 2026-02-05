# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    
    # URLs de autenticação - é incluido várias URLs de autenticação através desta rota ex: login, logout, password_change, password_change/done, password_reset, password_reset/done, password_reset/confirm, password_reset/complete
    path('accounts/', include('django.contrib.auth.urls')), 

    # URLs da APP accounts
    path('', include('accounts.urls')),

    # URLs da APP core
    path('', include('core.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
