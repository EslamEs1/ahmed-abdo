from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductImage, Size, Color, 
    ProductVariant, Review, Collection, Offer
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "لا توجد صورة"
    image_preview.short_description = "معاينة الصورة"

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'price', 'stock', 'is_active')

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('name', 'email', 'rating', 'comment', 'is_approved', 'created_at')
    readonly_fields = ('name', 'email', 'rating', 'comment', 'created_at')
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'parent', 'is_active', 'category_image')
    list_filter = ('is_active', 'parent')
    search_fields = ('name_ar', 'name_en')
    prepopulated_fields = {'slug': ('name_en',)}
    list_editable = ('is_active',)
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name_ar', 'name_en', 'slug', 'parent', 'is_active')
        }),
        ('الصورة', {
            'fields': ('image',),
        }),
    )
    
    def category_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "لا توجد صورة"
    category_image.short_description = "الصورة"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'price', 'old_price', 'discount_percentage', 'category', 'is_active', 'is_featured', 'is_on_sale', 'product_image')
    list_filter = ('is_active', 'is_featured', 'is_on_sale', 'category')
    search_fields = ('name_ar', 'name_en', 'description_ar', 'description_en')
    prepopulated_fields = {'slug': ('name_en',)}
    inlines = [ProductImageInline, ProductVariantInline, ReviewInline]
    list_editable = ('is_active', 'is_featured', 'is_on_sale', 'price')
    list_per_page = 20
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name_ar', 'name_en', 'slug', 'category')
        }),
        ('الأسعار', {
            'fields': ('price', 'old_price'),
        }),
        ('الوصف', {
            'fields': ('description_ar', 'description_en'),
        }),
        ('الخيارات', {
            'fields': ('is_active', 'is_featured', 'is_new', 'is_on_sale', 'badge'),
        }),
    )
    
    def discount_percentage(self, obj):
        if obj.get_discount_percentage() > 0:
            return f"{obj.get_discount_percentage()}%"
        return "-"
    discount_percentage.short_description = "نسبة الخصم"
    
    def product_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', main_image.image.url)
        return "لا توجد صورة"
    product_image.short_description = "الصورة"

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name')
    search_fields = ('name', 'name_ar')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name', 'color_preview')
    search_fields = ('name', 'name_ar')
    
    def color_preview(self, obj):
        return format_html('<div style="background-color: {}; width: 30px; height: 30px; border-radius: 5px;"></div>', obj.code)
    color_preview.short_description = "اللون"

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'size', 'color')
    search_fields = ('product__name_ar', 'product__name_en', 'sku')
    list_editable = ('price', 'stock', 'is_active')
    autocomplete_fields = ['product']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'rating_stars', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name_ar', 'product__name_en', 'name', 'email', 'comment')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return stars
    rating_stars.short_description = "التقييم"

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'is_active', 'created_at', 'collection_image', 'product_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_ar', 'name_en', 'description_ar', 'description_en')
    prepopulated_fields = {'slug': ('name_en',)}
    filter_horizontal = ('products',)
    list_editable = ('is_active',)
    
    def collection_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "لا توجد صورة"
    collection_image.short_description = "الصورة"
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "عدد المنتجات"

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title_ar', 'discount_percentage', 'start_date', 'end_date', 'is_active', 'offer_image', 'product_count')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title_ar', 'title_en', 'description_ar', 'description_en')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('products',)
    list_editable = ('discount_percentage', 'is_active')
    
    def offer_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "لا توجد صورة"
    offer_image.short_description = "الصورة"
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "عدد المنتجات"
