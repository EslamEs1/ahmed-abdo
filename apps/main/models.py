from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

class Slider(models.Model):
    """Model for managing website banner sliders"""
    PAGE_CHOICES = (
        ('home', _('الصفحة الرئيسية')),
        ('men', _('صفحة الرجال')),
        ('women', _('صفحة النساء')),
        ('kids', _('صفحة الأطفال')),

    )
    
    title = models.CharField(_("العنوان"), max_length=100)
    title_en = models.CharField(_("العنوان بالإنجليزية"), max_length=100, blank=True, null=True)
    title_ar = models.CharField(_("العنوان بالعربية"), max_length=100)
    subtitle = models.CharField(_("العنوان الفرعي"), max_length=200, blank=True, null=True)
    subtitle_en = models.CharField(_("العنوان الفرعي بالإنجليزية"), max_length=200, blank=True, null=True)
    subtitle_ar = models.CharField(_("العنوان الفرعي بالعربية"), max_length=200, blank=True, null=True)
    description = models.TextField(_("الوصف"), blank=True, null=True)
    description_en = models.TextField(_("الوصف بالإنجليزية"), blank=True, null=True)
    description_ar = models.TextField(_("الوصف بالعربية"), blank=True, null=True)
    image = models.ImageField(_("الصورة"), upload_to='sliders/')
    link = models.URLField(_("الرابط"), blank=True, null=True)
    link_text = models.CharField(_("نص الرابط"), max_length=50, blank=True, null=True)
    link_text_ar = models.CharField(_("نص الرابط بالعربية"), max_length=50, blank=True, null=True)
    page = models.CharField(_("الصفحة"), max_length=20, choices=PAGE_CHOICES, default='home')
    order = models.PositiveSmallIntegerField(_("الترتيب"), default=0)
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    
    class Meta:
        verbose_name = _("سلايدر")
        verbose_name_plural = _("السلايدرز")
        ordering = ['page', 'order']
    
    def __str__(self):
        return f"{self.title_ar} - {self.get_page_display()}"
