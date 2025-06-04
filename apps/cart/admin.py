from django.contrib import admin
from .models import Cart, CartItem, Coupon

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'items_count', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_id']
    inlines = [CartItemInline]
    readonly_fields = ['total_price', 'total_discount', 'final_price', 'items_count']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'variant', 'quantity', 'unit_price', 'total_price']
    list_filter = ['created_at']
    search_fields = ['cart__user__username', 'product__name', 'product__name_ar']
    readonly_fields = ['unit_price', 'total_price', 'discount']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_value', 'is_percentage', 'is_active', 'start_date', 'end_date', 'used_count']
    list_filter = ['is_active', 'is_percentage', 'created_at']
    search_fields = ['code', 'description']
    readonly_fields = ['used_count']
