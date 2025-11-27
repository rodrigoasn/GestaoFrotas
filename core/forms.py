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
            'session_timeout_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
