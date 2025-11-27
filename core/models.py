# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.db import models
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# MODEL: SYSTEM CONFIGURATION - SINGLETON
# ────────────────────────────────────────────────────────────────────
class SystemConfiguration(models.Model):
    session_timeout_minutes = models.PositiveIntegerField(
        default=30,
        help_text=_("Tempo em minutos de inatividade antes da sessão expirar.")
    )

    class Meta:
        verbose_name = _("Configuração do Sistema")
        verbose_name_plural = _("Configurações do Sistema")

    # save implementado para que não seja possível criar mais de uma configuração
    def save(self, *args, **kwargs):
        if not self.pk and SystemConfiguration.objects.exists():
            # If you want to prevent creating more than one object
            return
        return super(SystemConfiguration, self).save(*args, **kwargs)

    # proíbe o delete da configuração
    def delete(self, *args, **kwargs):
        return

    def __str__(self):
        return _("Configuração do Sistema")
