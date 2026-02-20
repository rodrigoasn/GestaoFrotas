# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from gestaoFrotas.mixins import AdminStaffRequiredMixin, SuperUserRequiredMixin, StaffOrPermissionRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, UserPermissionsForm, GroupForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Count


# ────────────────────────────────────────────────────────────────────
# USERS CRUD
# ────────────────────────────────────────────────────────────────────
# LISTVIEW
class UserListView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    permission_required = 'accounts.view_customuser'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(email__icontains=search_term)
        return queryset.order_by('email')

# CREATEVIEW
class UserCreateView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'accounts.add_customuser'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('Usuário criado com sucesso!'))
        return super().form_valid(form)

# UPDATEVIEW
class UserUpdateView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'accounts.change_customuser'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('Usuário atualizado com sucesso!'))
        return super().form_valid(form)

# DELETEVIEW
class UserDeleteView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'accounts.delete_customuser'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Usuário excluído com sucesso!'))
        return super().delete(request, *args, **kwargs)


# ────────────────────────────────────────────────────────────────────
# PASSWORD CHANGE
# ────────────────────────────────────────────────────────────────────
class UserPasswordChangeView(LoginRequiredMixin, StaffOrPermissionRequiredMixin, PasswordChangeView):
    """
    View para administrador alterar a senha de outro usuário.
    Usa o SetPasswordForm que não pede a senha antiga.
    """
    template_name = 'accounts/user_password_form.html'
    form_class = SetPasswordForm
    permission_required = 'accounts.change_customuser'
    
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


# ────────────────────────────────────────────────────────────────────
# USER PERMISSIONS VIEW (APENAS SUPERUSUÁRIOS E STAFF)
# ────────────────────────────────────────────────────────────────────
class UserPermissionsView(LoginRequiredMixin, AdminStaffRequiredMixin, UpdateView):
    """
    View para gerenciar grupos e permissões individuais de um usuário.
    Acessível apenas por superusuários e staff.
    """
    model = CustomUser
    form_class = UserPermissionsForm
    template_name = 'accounts/user_permissions.html'

    def get_success_url(self):
        messages.success(self.request, _('Permissões atualizadas com sucesso!'))
        return reverse_lazy('user_permissions', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa a lista de permissões agrupada por app_label para o template
        form = context['form']
        permissions_by_app = {}
        for perm in form.fields['user_permissions'].queryset:
            app_label = perm.content_type.app_label
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {
                    'models': {}
                }
            model_name = perm.content_type.model
            if model_name not in permissions_by_app[app_label]['models']:
                permissions_by_app[app_label]['models'][model_name] = {
                    'name': perm.content_type.name,
                    'permissions': []
                }
            permissions_by_app[app_label]['models'][model_name]['permissions'].append(perm)
        context['permissions_by_app'] = permissions_by_app
        # Obtém os IDs das permissões já atribuídas ao usuário
        context['user_permission_ids'] = set(
            self.get_object().user_permissions.values_list('id', flat=True)
        )
        context['user_group_ids'] = set(
            self.get_object().groups.values_list('id', flat=True)
        )
        # Protege contra edição das próprias permissões
        context['is_self'] = self.get_object() == self.request.user
        return context


# ────────────────────────────────────────────────────────────────────
# GROUPS CRUD (ADMIN E STAFF)
# ────────────────────────────────────────────────────────────────────
# LISTVIEW 
class GroupListView(LoginRequiredMixin, AdminStaffRequiredMixin, ListView):
    model = Group
    template_name = 'accounts/group_list.html'
    context_object_name = 'groups'
    ordering = ['name']

    def get_queryset(self):
        # Anota cada grupo com a contagem de membros e permissões
        return Group.objects.annotate(
            members_count=Count('user', distinct=True),
            permissions_count=Count('permissions', distinct=True),
        ).order_by('name')

# CREATEVIEW
class GroupCreateView(LoginRequiredMixin, AdminStaffRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_form.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions_by_app'] = self._build_permissions_by_app(context['form'])
        context['group_permission_ids'] = set()
        return context

    def _build_permissions_by_app(self, form):
        permissions_by_app = {}
        for perm in form.fields['permissions'].queryset:
            app_label = perm.content_type.app_label
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {'models': {}}
            model_name = perm.content_type.model
            if model_name not in permissions_by_app[app_label]['models']:
                permissions_by_app[app_label]['models'][model_name] = {
                    'name': perm.content_type.name,
                    'permissions': []
                }
            permissions_by_app[app_label]['models'][model_name]['permissions'].append(perm)
        return permissions_by_app

    def form_valid(self, form):
        messages.success(self.request, _('Grupo criado com sucesso!'))
        return super().form_valid(form)

# UPDATEVIEW
class GroupUpdateView(LoginRequiredMixin, AdminStaffRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_form.html'

    def get_success_url(self):
        return reverse_lazy('group_change', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions_by_app'] = self._build_permissions_by_app(context['form'])
        context['group_permission_ids'] = set(
            self.get_object().permissions.values_list('id', flat=True)
        )
        return context

    def _build_permissions_by_app(self, form):
        permissions_by_app = {}
        for perm in form.fields['permissions'].queryset:
            app_label = perm.content_type.app_label
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {'models': {}}
            model_name = perm.content_type.model
            if model_name not in permissions_by_app[app_label]['models']:
                permissions_by_app[app_label]['models'][model_name] = {
                    'name': perm.content_type.name,
                    'permissions': []
                }
            permissions_by_app[app_label]['models'][model_name]['permissions'].append(perm)
        return permissions_by_app

    def form_valid(self, form):
        messages.success(self.request, _('Grupo atualizado com sucesso!'))
        return super().form_valid(form)

# DELETEVIEW
class GroupDeleteView(LoginRequiredMixin, AdminStaffRequiredMixin, DeleteView):
    model = Group
    template_name = 'accounts/group_confirm_delete.html'
    success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        messages.success(self.request, _('Grupo excluído com sucesso!'))
        return super().form_valid(form)
