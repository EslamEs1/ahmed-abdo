from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_read = models.BooleanField(_('Is Read'), default=False)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class ContactInfo(models.Model):
    """Model for storing contact information displayed on the contact page"""
    address = models.CharField(_('Address'), max_length=200)
    phone = models.CharField(_('Phone'), max_length=20)
    email = models.EmailField(_('Email'))
    map_url = models.URLField(_('Google Maps URL'), max_length=500, help_text=_('Google Maps embed URL'))
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Contact Information')
        verbose_name_plural = _('Contact Information')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Ensure only one active contact info exists
        if self.is_active:
            ContactInfo.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)
