from django.contrib import admin
from .models import Order, OrderItem, OrderTracker, ShippingAddress

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'discount']

class OrderTrackerInline(admin.TabularInline):
    model = OrderTracker
    extra = 0
    max_num = 10
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'phone', 'city', 'status', 'payment_status', 
                   'order_total', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['order_number', 'ip_address', 'total_price', 'final_price']
    inlines = [OrderItemInline, OrderTrackerInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Order Information', {
            'fields': ('order_number', 'order_total', 'discount', 'shipping_cost', 'order_note', 'status', 'is_ordered')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'area')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'payment_reference', 'payment_screenshot')
        }),
        ('Additional Information', {
            'fields': ('ip_address', 'coupon', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'city', 'area', 'is_default']
    list_filter = ['city', 'is_default', 'created_at']
    search_fields = ['user__username', 'first_name', 'last_name', 'address']
