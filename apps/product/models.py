from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Category model for product classification"""
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True)
    name_ar = models.CharField(_("Arabic Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=120)
    image = models.ImageField(_("Image"), upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, 
                              related_name='children', verbose_name=_("Parent Category"))
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
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
        ('new', _('New')),
        ('sale', _('Sale')),
        ('hot', _('Hot')),
        ('exclusive', _('Exclusive')),
    )
    
    name = models.CharField(_("Name"), max_length=200)
    name_en = models.CharField(_("English Name"), max_length=200, blank=True)
    name_ar = models.CharField(_("Arabic Name"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, max_length=255)
    description = models.TextField(_("Description"), blank=True)
    description_en = models.TextField(_("English Description"), blank=True)
    description_ar = models.TextField(_("Arabic Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    old_price = models.DecimalField(_("Old Price"), max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_("Category"))
    badge = models.CharField(_("Badge"), max_length=20, choices=BADGE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_featured = models.BooleanField(_("Featured"), default=False)
    is_new = models.BooleanField(_("New"), default=False)
    is_on_sale = models.BooleanField(_("On Sale"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("Product"))
    image = models.ImageField(_("Image"), upload_to='products/')
    is_main = models.BooleanField(_("Main Image"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['-is_main', 'created_at']
    
    def __str__(self):
        return f"Image for {self.product.name_ar}"


class Size(models.Model):
    """Size model for products"""
    name = models.CharField(_("Name"), max_length=20)
    name_ar = models.CharField(_("Arabic Name"), max_length=20)
    
    class Meta:
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")
        ordering = ['name']
    
    def __str__(self):
        return self.name_ar


class Color(models.Model):
    """Color model for products"""
    name = models.CharField(_("Name"), max_length=50)
    name_ar = models.CharField(_("Arabic Name"), max_length=50)
    code = models.CharField(_("Color Code"), max_length=10, help_text="Hex color code e.g. #FF0000")
    
    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")
        ordering = ['name']
    
    def __str__(self):
        return self.name_ar


class ProductVariant(models.Model):
    """Product variant model for different sizes and colors"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_("Product"))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=_("Size"))
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=_("Color"))
    sku = models.CharField(_("SKU"), max_length=100, unique=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(_("Stock"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)
    
    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        unique_together = ['product', 'size', 'color']
    
    def __str__(self):
        return f"{self.product.name_ar} - {self.size.name_ar} - {self.color.name_ar}"


class Review(models.Model):
    """Product review model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Product"))
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"), max_length=100)
    rating = models.PositiveSmallIntegerField(_("Rating"), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    is_approved = models.BooleanField(_("Approved"), default=False)
    
    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.name} on {self.product.name_ar}"


class Collection(models.Model):
    """Special collections model for featured product groups"""
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, blank=True)
    name_ar = models.CharField(_("Arabic Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=120)
    description = models.TextField(_("Description"), blank=True)
    description_en = models.TextField(_("English Description"), blank=True)
    description_ar = models.TextField(_("Arabic Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='collections/')
    products = models.ManyToManyField(Product, related_name='collections', verbose_name=_("Products"))
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
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
    title = models.CharField(_("Title"), max_length=200)
    title_en = models.CharField(_("English Title"), max_length=200, blank=True)
    title_ar = models.CharField(_("Arabic Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, max_length=255)
    description = models.TextField(_("Description"), blank=True)
    description_en = models.TextField(_("English Description"), blank=True)
    description_ar = models.TextField(_("Arabic Description"), blank=True)
    discount_percentage = models.PositiveIntegerField(_("Discount Percentage"), default=0)
    image = models.ImageField(_("Image"), upload_to='offers/', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='offers', verbose_name=_("Products"))
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title_ar
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:offer_detail', kwargs={'slug': self.slug})
