from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title_ar', 'page_display', 'order', 'is_active')
    list_filter = ('page', 'is_active', 'created_at')
    search_fields = ('title_ar', 'title_en', 'subtitle_ar', 'subtitle_en', 'description_ar', 'description_en')
    list_editable = ('order', 'is_active')
    list_per_page = 10
    save_on_top = True
    
    fieldsets = (
        (_('معلومات العرض'), {
            'fields': ('is_active', 'page', 'order'),
            'classes': ('wide',),
        }),
        (_('النص والعناوين'), {
            'fields': (
                'title_ar', 'title_en',
                'subtitle_ar', 'subtitle_en',
                'description_ar', 'description_en',
            ),
            'classes': ('wide',),
        }),
        (_('الصورة'), {
            'fields': ('image', 'image_preview'),
            'classes': ('wide',),
        }),
        (_('الرابط'), {
            'fields': ('link', 'link_text_ar', 'link_text'),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    readonly_fields = ('image_preview',)
    
    def page_display(self, obj):
        """Display the page name in Arabic"""
        return obj.get_page_display()
    page_display.short_description = _("الصفحة")
    
    def image_preview(self, obj):
        """Display a preview of the slider image"""
        if obj.image:
            return format_html('<img src="{}" width="150" height="80" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return _("لا توجد صورة")
    image_preview.short_description = _("معاينة الصورة")
