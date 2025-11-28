# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import SystemConfiguration
from .forms import SystemConfigurationForm
from django.http import JsonResponse


# ────────────────────────────────────────────────────────────────────
# VIEWS: CONFIGURAÇÕES
# ────────────────────────────────────────────────────────────────────
class SettingsView(LoginRequiredMixin, View):
    template_name = 'core/settings.html'

    def get_object(self):
        # Garante que apenas uma instância exista
        obj, created = SystemConfiguration.objects.get_or_create(pk=1)
        return obj

    def get(self, request):
        config = self.get_object()
        form = SystemConfigurationForm(instance=config)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        config = self.get_object()
        form = SystemConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, _('Configurações atualizadas com sucesso!'))
            return redirect('settings')
        
        messages.error(request, _('Erro ao atualizar configurações.'))
        return render(request, self.template_name, {'form': form})