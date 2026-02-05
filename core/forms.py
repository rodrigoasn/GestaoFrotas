# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django import forms
from .models import SystemConfiguration
from django.utils.translation import gettext as _


# ────────────────────────────────────────────────────────────────────
# FORMS: CONFIGURAÇÕES
# ────────────────────────────────────────────────────────────────────
class SystemConfigurationForm(forms.ModelForm):
    class Meta:
        model = SystemConfiguration
        fields = [
            'session_timeout_minutes', 
            'image_logo', 'image_login_banner', 'image_favicon', 'image_background',
            'cnpj', 'inscricao_estadual', 'razao_social', 'nome_fantasia',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'email_principal', 'telefone_principal', 'whatsapp',
            'website', 'linkedin', 'facebook', 'instagram', 'twitter', 'youtube'
        ]
        widgets = {
            'session_timeout_minutes': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '2',
                'onblur': 'if(this.value < 2) this.value = 2;'
            }),
            'image_logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_login_banner': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_favicon': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_background': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            
            # Company Info
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            
            # Contact
            'email_principal': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            
            # Social
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
        }
        help_texts = {
            'image_logo': _('Deixe vazio para manter a logo atual.'),
            'image_login_banner': _('Deixe vazio para manter o banner atual.'),
            'image_favicon': _('Deixe vazio para manter o favicon atual.'),
            'image_background': _('Deixe vazio para manter o background atual.'),
        }

    # Trava a configuração para que não seja possível configurar um tempo de sessão menor que 2 minutos via formulário burlando as validações do HTML (server side)
    def clean_session_timeout_minutes(self):
        minutes = self.cleaned_data.get('session_timeout_minutes')
        if minutes is not None and minutes < 2:
            raise forms.ValidationError(_("O tempo de sessão deve ser de no mínimo 2 minutos."))
        return minutes
