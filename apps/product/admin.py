from django.contrib import admin
from .models import (
    Category, Product, ProductImage, Size, Color, 
    ProductVariant, Review, Collection, Offer
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('name', 'email', 'rating', 'comment', 'created_at')
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name_ar', 'name_en')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'price', 'old_price', 'category', 'is_active', 'is_featured', 'is_on_sale')
    list_filter = ('is_active', 'is_featured', 'is_on_sale', 'category')
    search_fields = ('name_ar', 'name_en', 'description_ar', 'description_en')
    prepopulated_fields = {'slug': ('name_en',)}
    inlines = [ProductImageInline, ProductVariantInline, ReviewInline]
    list_editable = ('is_active', 'is_featured', 'is_on_sale')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar')
    search_fields = ('name', 'name_ar')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'code')
    search_fields = ('name', 'name_ar')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'size', 'color')
    search_fields = ('product__name_ar', 'product__name_en', 'sku')
    list_editable = ('price', 'stock', 'is_active')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name_ar', 'product__name_en', 'name', 'email', 'comment')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_ar', 'name_en', 'description_ar', 'description_en')
    prepopulated_fields = {'slug': ('name_en',)}
    filter_horizontal = ('products',)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title_ar', 'title_en', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title_ar', 'title_en', 'description_ar', 'description_en')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('products',)
    list_editable = ('discount_percentage', 'is_active')
