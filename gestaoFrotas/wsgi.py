# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
import os
from django.core.wsgi import get_wsgi_application


# ────────────────────────────────────────────────────────────────────
# WSGI
# ────────────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestaoFrotas.settings')

application = get_wsgi_application()
