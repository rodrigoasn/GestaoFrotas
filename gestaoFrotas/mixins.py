# ────────────────────────────────────────────────────────────────────
# MIXINS GLOBAIS
# Importável de qualquer app: from gestaoFrotas.mixins import ...
# ────────────────────────────────────────────────────────────────────
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminStaffRequiredMixin(UserPassesTestMixin):
    """Permite acesso apenas a superusuários ou membros da equipe (is_staff)."""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class SuperUserRequiredMixin(UserPassesTestMixin):
    """Permite acesso apenas a superusuários."""
    def test_func(self):
        return self.request.user.is_superuser


class StaffOrPermissionRequiredMixin(UserPassesTestMixin):
    """
    Permite acesso a:
      - Superusuários (acesso irrestrito)
      - Membros da equipe is_staff
      - Usuários comuns que possuam a permissão Django definida em `permission_required`

    Uso na view:
        class MinhaView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, ...):
            permission_required = 'app.action_modelo'  # ou lista de perms
    """
    permission_required = None  # Ex: 'accounts.view_customuser'

    def test_func(self):
        user = self.request.user
        # Superusers e staff sempre têm acesso
        if user.is_superuser or user.is_staff:
            return True
        # Verifica permissão individual (suporte a string ou lista)
        if self.permission_required:
            if isinstance(self.permission_required, (list, tuple)):
                return any(user.has_perm(p) for p in self.permission_required)
            return user.has_perm(self.permission_required)
        return False

