# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from gestaoFrotas.mixins import AdminStaffRequiredMixin, StaffOrPermissionRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import SystemConfiguration
from .forms import SystemConfigurationForm
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .helpers import buscar_cnpj_receitaws, buscar_cep_viacep


# ────────────────────────────────────────────────────────────────────
# DASHBOARD VIEW
# ────────────────────────────────────────────────────────────────────
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


# ────────────────────────────────────────────────────────────────────
# VIEW: SERVICE WORKER
# ────────────────────────────────────────────────────────────────────
@method_decorator(cache_control(max_age=60 * 60 * 24, immutable=True, public=True), name='dispatch')
class ServiceWorkerView(TemplateView):
    template_name = 'service-worker.js'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/javascript'
        return super().render_to_response(context, **response_kwargs)


# ────────────────────────────────────────────────────────────────────
# VIEWS: CONFIGURAÇÕES
# ────────────────────────────────────────────────────────────────────
class SettingsView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, View):
    template_name = 'core/settings.html'
    permission_required = 'core.change_systemconfiguration'

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
        form = SystemConfigurationForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, _('Configurações atualizadas com sucesso!'))
            return redirect('settings')
        
        messages.error(request, _('Erro ao atualizar configurações.'))
        return render(request, self.template_name, {'form': form})


# ────────────────────────────────────────────────────────────────────
# VIEW: API CNPJ SEARCH
# ────────────────────────────────────────────────────────────────────
class CNPJSearchView(LoginRequiredMixin, View):
    def get(self, request, cnpj):
        data = buscar_cnpj_receitaws(cnpj)
        
        if "erro" in data:
            return JsonResponse(data, status=400 if "inválido" in data["erro"].lower() else 500)
            
        return JsonResponse(data)


# ────────────────────────────────────────────────────────────────────
# VIEW: API CEP SEARCH
# ────────────────────────────────────────────────────────────────────
class CEPSearchView(LoginRequiredMixin, View):
    def get(self, request, cep):
        data = buscar_cep_viacep(cep)
        
        if "erro" in data:
            return JsonResponse(data, status=400 if "inválido" in data["erro"].lower() else 500)
            
        return JsonResponse(data)
