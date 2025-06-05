from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
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
    whatsapp = models.CharField(_('WhatsApp'), max_length=20, blank=True, null=True)
    email = models.EmailField(_('Email'))
    working_hours = models.CharField(_('Working Hours'), max_length=100, blank=True, null=True)
    google_map_url = models.URLField(_('Google Maps URL'), max_length=500, blank=True, null=True)
    facebook = models.URLField(_('Facebook'), blank=True, null=True)
    instagram = models.URLField(_('Instagram'), blank=True, null=True)
    twitter = models.URLField(_('Twitter'), blank=True, null=True)
    tiktok = models.URLField(_('TikTok'), blank=True, null=True)
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

class Newsletter(models.Model):
    """Store newsletter subscribers"""
    email = models.EmailField(_('البريد الإلكتروني'), unique=True)
    active = models.BooleanField(_('نشط'), default=True)
    created_at = models.DateTimeField(_('تاريخ الاشتراك'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('اشتراك النشرة البريدية')
        verbose_name_plural = _('اشتراكات النشرة البريدية')
        ordering = ['-created_at']
        
    def __str__(self):
        return self.email
