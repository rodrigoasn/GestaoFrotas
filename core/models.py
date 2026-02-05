# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.db import models
from django.utils.translation import gettext_lazy as _


# ────────────────────────────────────────────────────────────────────
# MODEL: SYSTEM CONFIGURATION - SINGLETON
# ────────────────────────────────────────────────────────────────────
class SystemConfiguration(models.Model):
    # Sessão
    session_timeout_minutes = models.PositiveIntegerField(
        default=30,
        help_text=_("Tempo em minutos de inatividade antes da sessão expirar.")
    )
    
    # Personalização
    image_logo = models.ImageField(upload_to='img/logo', blank=True, null=True)
    image_login_banner = models.ImageField(upload_to='img/login_banner', blank=True, null=True)
    image_favicon = models.ImageField(upload_to='img/favicon', blank=True, null=True)
    image_background = models.ImageField(upload_to='img/background', blank=True, null=True)
    
    # Informações da Empresa
    cnpj = models.CharField(_("CNPJ"), max_length=20, blank=True, null=True)
    inscricao_estadual = models.CharField(_("Inscrição Estadual"), max_length=20, blank=True, null=True)
    razao_social = models.CharField(_("Razão Social"), max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(_("Nome Fantasia"), max_length=255, blank=True, null=True)
    cep = models.CharField(_("CEP"), max_length=10, blank=True, null=True)
    endereco = models.CharField(_("Endereço"), max_length=255, blank=True, null=True)
    numero = models.CharField(_("Número"), max_length=10, blank=True, null=True)
    complemento = models.CharField(_("Complemento"), max_length=255, blank=True, null=True)
    
    UF_CHOICES = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'),
        ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'),
        ('SE', 'Sergipe'), ('TO', 'Tocantins')
    )
    estado = models.CharField(_("Estado/Província"), max_length=2, choices=UF_CHOICES, blank=True, null=True)
    cidade = models.CharField(_("Cidade"), max_length=100, blank=True, null=True)
    bairro = models.CharField(_("Bairro"), max_length=100, blank=True, null=True)
    
    # Contato
    email_principal = models.EmailField(_("Email Principal"), blank=True, null=True)
    telefone_principal = models.CharField(_("Telefone de Contato Principal"), max_length=20, blank=True, null=True)
    whatsapp = models.CharField(_("WhatsApp"), max_length=20, blank=True, null=True)
    
    # Redes Sociais
    website = models.URLField(_("Website"), blank=True, null=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True, null=True)
    facebook = models.URLField(_("Facebook"), blank=True, null=True)
    instagram = models.URLField(_("Instagram"), blank=True, null=True)
    twitter = models.URLField(_("Twitter"), blank=True, null=True)
    youtube = models.URLField(_("YouTube"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Configuração do Sistema")
        verbose_name_plural = _("Configurações do Sistema")

    # save implementado para que não seja possível criar mais de uma configuração
    def save(self, *args, **kwargs):
        if not self.pk and SystemConfiguration.objects.exists():
            # Se você quiser prevenir a criação de mais de um objeto
            return
        return super(SystemConfiguration, self).save(*args, **kwargs)

    # proíbe o delete da configuração
    def delete(self, *args, **kwargs):
        return

    def __str__(self):
        return _("Configuração do Sistema")
