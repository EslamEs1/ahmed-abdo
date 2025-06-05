from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Category model for product classification"""
    name = models.CharField(_("الاسم"), max_length=100)
    name_en = models.CharField(_("الاسم بالإنجليزية"), max_length=100, blank=True)
    name_ar = models.CharField(_("الاسم بالعربية"), max_length=100)
    slug = models.SlugField(_("الرابط"), unique=True, max_length=120)
    image = models.ImageField(_("الصورة"), upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, 
                              related_name='children', verbose_name=_("القسم الرئيسي"))
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    
    class Meta:
        verbose_name = _("قسم")
        verbose_name_plural = _("الأقسام")
        ordering = ['name']
    
    def __str__(self):
        return self.name_ar
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """Product model"""
    BADGE_CHOICES = (
        ('new', _('جديد')),
        ('sale', _('تخفيض')),
        ('hot', _('رائج')),
        ('exclusive', _('حصري')),
    )
    
    name = models.CharField(_("الاسم"), max_length=200)
    name_en = models.CharField(_("الاسم بالإنجليزية"), max_length=200, blank=True)
    name_ar = models.CharField(_("الاسم بالعربية"), max_length=200)
    slug = models.SlugField(_("الرابط"), unique=True, max_length=255)
    description = models.TextField(_("الوصف"), blank=True)
    description_en = models.TextField(_("الوصف بالإنجليزية"), blank=True)
    description_ar = models.TextField(_("الوصف بالعربية"), blank=True)
    price = models.DecimalField(_("السعر الحالي"), max_digits=10, decimal_places=2)
    old_price = models.DecimalField(_("السعر القديم"), max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_("القسم"))
    badge = models.CharField(_("الشارة"), max_length=20, choices=BADGE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(_("نشط"), default=True)
    is_featured = models.BooleanField(_("مميز"), default=False)
    is_new = models.BooleanField(_("جديد"), default=False)
    is_on_sale = models.BooleanField(_("عرض خاص"), default=False)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    
    class Meta:
        verbose_name = _("منتج")
        verbose_name_plural = _("المنتجات")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name_ar
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})
    
    def get_discount_percentage(self):
        if self.old_price and self.price < self.old_price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    """Product images model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("المنتج"))
    image = models.ImageField(_("الصورة"), upload_to='products/')
    is_main = models.BooleanField(_("صورة رئيسية"), default=False)
    created_at = models.DateTimeField(_("تاريخ الإضافة"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("صورة المنتج")
        verbose_name_plural = _("صور المنتجات")
        ordering = ['-is_main', 'created_at']
    
    def __str__(self):
        return f"صورة لمنتج {self.product.name_ar}"


class Size(models.Model):
    """Size model for products"""
    name = models.CharField(_("الاسم بالإنجليزية"), max_length=20)
    name_ar = models.CharField(_("الاسم بالعربية"), max_length=20)
    
    class Meta:
        verbose_name = _("المقاس")
        verbose_name_plural = _("المقاسات")
        ordering = ['name']
    
    def __str__(self):
        return self.name_ar


class Color(models.Model):
    """Color model for products"""
    name = models.CharField(_("الاسم بالإنجليزية"), max_length=50)
    name_ar = models.CharField(_("الاسم بالعربية"), max_length=50)
    code = models.CharField(_("كود اللون"), max_length=10, help_text=_("كود اللون بصيغة hex مثل #FF0000"))
    
    class Meta:
        verbose_name = _("اللون")
        verbose_name_plural = _("الألوان")
        ordering = ['name']
    
    def __str__(self):
        return self.name_ar


class ProductVariant(models.Model):
    """Product variant model for different sizes and colors"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_("المنتج"))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=_("المقاس"))
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=_("اللون"))
    sku = models.CharField(_("رمز المنتج"), max_length=100, unique=True)
    price = models.DecimalField(_("السعر الخاص"), max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(_("الكمية المتوفرة"), default=0)
    is_active = models.BooleanField(_("نشط"), default=True)
    
    class Meta:
        verbose_name = _("نسخة المنتج")
        verbose_name_plural = _("نسخ المنتجات")
        unique_together = ['product', 'size', 'color']
    
    def __str__(self):
        return f"{self.product.name_ar} - {self.size.name_ar} - {self.color.name_ar}"


class Review(models.Model):
    """Product review model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("المنتج"))
    name = models.CharField(_("الاسم"), max_length=100)
    email = models.EmailField(_("البريد الإلكتروني"), max_length=100)
    rating = models.PositiveSmallIntegerField(_("التقييم"), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_("التعليق"))
    created_at = models.DateTimeField(_("تاريخ الإضافة"), auto_now_add=True)
    is_approved = models.BooleanField(_("معتمد"), default=False)
    
    class Meta:
        verbose_name = _("تقييم")
        verbose_name_plural = _("التقييمات")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"تقييم من {self.name} على {self.product.name_ar}"


class Collection(models.Model):
    """Special collections model for featured product groups"""
    name = models.CharField(_("الاسم"), max_length=100)
    name_en = models.CharField(_("الاسم بالإنجليزية"), max_length=100, blank=True)
    name_ar = models.CharField(_("الاسم بالعربية"), max_length=100)
    slug = models.SlugField(_("الرابط"), unique=True, max_length=120)
    description = models.TextField(_("الوصف"), blank=True)
    description_en = models.TextField(_("الوصف بالإنجليزية"), blank=True)
    description_ar = models.TextField(_("الوصف بالعربية"), blank=True)
    image = models.ImageField(_("الصورة"), upload_to='collections/')
    products = models.ManyToManyField(Product, related_name='collections', verbose_name=_("المنتجات"))
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("تشكيلة")
        verbose_name_plural = _("التشكيلات")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name_ar
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:collection_detail', kwargs={'slug': self.slug})


class Offer(models.Model):
    """Special offers and promotions model"""
    title = models.CharField(_("العنوان"), max_length=200)
    title_en = models.CharField(_("العنوان بالإنجليزية"), max_length=200, blank=True)
    title_ar = models.CharField(_("العنوان بالعربية"), max_length=200)
    slug = models.SlugField(_("الرابط"), unique=True, max_length=255)
    description = models.TextField(_("الوصف"), blank=True)
    description_en = models.TextField(_("الوصف بالإنجليزية"), blank=True)
    description_ar = models.TextField(_("الوصف بالعربية"), blank=True)
    discount_percentage = models.PositiveIntegerField(_("نسبة الخصم"), default=0)
    image = models.ImageField(_("صورة العرض"), upload_to='offers/', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='offers', verbose_name=_("المنتجات"))
    start_date = models.DateTimeField(_("تاريخ البدء"))
    end_date = models.DateTimeField(_("تاريخ الانتهاء"))
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("عرض")
        verbose_name_plural = _("العروض")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title_ar
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:offer_detail', kwargs={'slug': self.slug})
