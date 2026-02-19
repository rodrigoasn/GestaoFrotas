# ────────────────────────────────────────────────────────────────────
# FORMS
# ────────────────────────────────────────────────────────────────────
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# ────────────────────────────────────────────────────────────────────
# USER CREATION FORMS 
# ────────────────────────────────────────────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        # Regras de Segurança
        if self.request_user and not self.request_user.is_superuser:
            if 'is_staff' in self.fields: del self.fields['is_staff']
            if 'is_superuser' in self.fields: del self.fields['is_superuser']
            if 'is_active' in self.fields: del self.fields['is_active']

# ────────────────────────────────────────────────────────────────────
# USER CHANGE FORMS 
# ────────────────────────────────────────────────────────────────────
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'avatar', 'is_staff', 'is_superuser', 'is_active')

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        
        # Remove o campo de senha padrão do Django 
        # foi criado um botão dedicado "Alterar Senha" no template.
        if 'password' in self.fields:
            del self.fields['password']

        # Regras de Segurança
        if self.request_user:
            # Regra 1: Se não for Superuser, não vê e não edita permissões
            if not self.request_user.is_superuser:
                if 'is_staff' in self.fields: del self.fields['is_staff']
                if 'is_superuser' in self.fields: del self.fields['is_superuser']
                if 'is_active' in self.fields: del self.fields['is_active']
            
            # Regra 2: Se for Superuser, mas estiver editando a si mesmo, não pode alterar suas próprias permissões (evitar lockout)
            elif self.instance == self.request_user:
                if 'is_staff' in self.fields: 
                    self.fields['is_staff'].disabled = True
                    self.fields['is_staff'].help_text = "Você não pode remover seu próprio acesso administrativo."
                if 'is_superuser' in self.fields: 
                    self.fields['is_superuser'].disabled = True
                    self.fields['is_superuser'].help_text = "Você não pode remover seu próprio acesso de superusuário."
                if 'is_active' in self.fields: 
                    self.fields['is_active'].disabled = True
                    self.fields['is_active'].help_text = "Você não pode desativar seu próprio usuário."

# ────────────────────────────────────────────────────────────────────
# USER PROFILE FORMS 
# ────────────────────────────────────────────────────────────────────
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'avatar')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].disabled = True
