from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, ContactInfo, Newsletter

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    fieldsets = (
        (_('معلومات المرسل'), {
            'fields': ('name', 'email', 'phone')
        }),
        (_('محتوى الرسالة'), {
            'fields': ('subject', 'message')
        }),
        (_('معلومات إضافية'), {
            'fields': ('created_at', 'is_read')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = ['mark_as_read', 'mark_as_unread']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'address')
    fieldsets = (
        (_('معلومات الاتصال الأساسية'), {
            'fields': ('email', 'phone', 'whatsapp', 'address', 'working_hours', 'google_map_url')
        }),
        (_('روابط التواصل الاجتماعي'), {
            'fields': ('facebook', 'instagram', 'twitter', 'tiktok')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion if only one contact info exists
        if ContactInfo.objects.count() <= 1:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, _("تم تفعيل اشتراك النشرة البريدية للمستخدمين المحددين بنجاح"))
    activate_subscribers.short_description = _("تفعيل اشتراك النشرة البريدية للمستخدمين المحددين")
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, _("تم إلغاء تفعيل اشتراك النشرة البريدية للمستخدمين المحددين بنجاح"))
    deactivate_subscribers.short_description = _("إلغاء تفعيل اشتراك النشرة البريدية للمستخدمين المحددين")
