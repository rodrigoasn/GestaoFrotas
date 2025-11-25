# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.db import models
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# MODEL: SYSTEM CONFIGURATION
# ────────────────────────────────────────────────────────────────────
class SystemConfiguration(models.Model):
    session_timeout_minutes = models.PositiveIntegerField(
        default=30,
        help_text=_("Time in minutes of inactivity before session expires.")
    )

    class Meta:
        verbose_name = _("System Configuration")
        verbose_name_plural = _("System Configurations")

    def save(self, *args, **kwargs):
        if not self.pk and SystemConfiguration.objects.exists():
            # If you want to prevent creating more than one object
            return
        return super(SystemConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return _("System Configuration")
