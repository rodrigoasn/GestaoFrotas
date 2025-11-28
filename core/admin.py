# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.contrib import admin
from .models import SystemConfiguration

# ────────────────────────────────────────────────────────────────────
# ADMIN: CONFIGURAÇÃO DO SISTEMA
# ────────────────────────────────────────────────────────────────────
@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Permite adicionar apenas se não houver instância
        if SystemConfiguration.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Proíbe a exclusão
        return False
