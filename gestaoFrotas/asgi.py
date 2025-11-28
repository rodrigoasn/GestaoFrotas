# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
import os
from django.core.asgi import get_asgi_application


# ────────────────────────────────────────────────────────────────────
# ASGI
# ────────────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestaoFrotas.settings')

application = get_asgi_application()
