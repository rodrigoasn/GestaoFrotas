# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordChangeView


# ────────────────────────────────────────────────────────────────────
# DASHBOARD VIEW
# ────────────────────────────────────────────────────────────────────
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


# ────────────────────────────────────────────────────────────────────
# USERS CRUD
# ────────────────────────────────────────────────────────────────────
# Mixin para garantir que apenas superusuários ou staff possam gerenciar usuários
class AdminStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# LISTVIEW
class UserListView(LoginRequiredMixin, AdminStaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(email__icontains=search_term)
        return queryset.order_by('email')

# CREATEVIEW
class UserCreateView(LoginRequiredMixin, AdminStaffRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, _('Usuário criado com sucesso!'))
        return super().form_valid(form)

# UPDATEVIEW
class UserUpdateView(LoginRequiredMixin, AdminStaffRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('Usuário atualizado com sucesso!'))
        return super().form_valid(form)

# DELETEVIEW
class UserDeleteView(LoginRequiredMixin, AdminStaffRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Usuário excluído com sucesso!'))
        return super().delete(request, *args, **kwargs)


# ────────────────────────────────────────────────────────────────────
# PASSWORD CHANGE (ADMIN)
# ────────────────────────────────────────────────────────────────────
class UserPasswordChangeView(LoginRequiredMixin, AdminStaffRequiredMixin, PasswordChangeView):
    """
    View para administrador alterar a senha de outro usuário.
    Usa o SetPasswordForm que não pede a senha antiga.
    """
    template_name = 'accounts/user_password_form.html'
    form_class = SetPasswordForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # O AdminPasswordChangeForm espera 'user' como primeiro argumento pro init, 
        # mas PasswordChangeView injeta request.user automaticamente. 
        # Precisamos sobrescrever para passar o usuário alvo (pela URL).
        kwargs['user'] = CustomUser.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = CustomUser.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        messages.success(self.request, _('Senha alterada com sucesso!'))
        return reverse_lazy('user_list')


# ────────────────────────────────────────────────────────────────────
# PROFILE VIEW
# ────────────────────────────────────────────────────────────────────
class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Perfil atualizado com sucesso!'))
        return super().form_valid(form)
