# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django import forms
from .models import SystemConfiguration


# ────────────────────────────────────────────────────────────────────
# FORMS: CONFIGURAÇÕES
# ────────────────────────────────────────────────────────────────────
class SystemConfigurationForm(forms.ModelForm):
    class Meta:
        model = SystemConfiguration
        fields = ['session_timeout_minutes']
        widgets = {
            'session_timeout_minutes': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '2',
                'onblur': 'if(this.value < 2) this.value = 2;'
            }),
        }

    # Trava a configuração para que não seja possível configurar um tempo de sessão menor que 2 minutos via formulário burlando as validações do HTML (server side)
    def clean_session_timeout_minutes(self):
        minutes = self.cleaned_data.get('session_timeout_minutes')
        if minutes is not None and minutes < 2:
            raise forms.ValidationError("O tempo de sessão deve ser de no mínimo 2 minutos.")
        return minutes
