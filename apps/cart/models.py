from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.product.models import Product, ProductVariant

class Cart(models.Model):
    """Shopping cart model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='carts', verbose_name=_("User"))
    session_id = models.CharField(_("Session ID"), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
    
    def __str__(self):
        return f"Cart {self.id} - {self.user or self.session_id}"
    
    @property
    def total_price(self):
        """Calculate the total price of all items in the cart"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_discount(self):
        """Calculate the total discount of all items in the cart"""
        return sum(item.discount for item in self.items.all())
    
    @property
    def final_price(self):
        """Calculate the final price after discount"""
        return self.total_price - self.total_discount
    
    @property
    def items_count(self):
        """Count the total number of items in the cart"""
        return self.items.count()


class CartItem(models.Model):
    """Shopping cart item model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name=_("Cart"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Variant"))
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        unique_together = ['cart', 'product', 'variant']
    
    def __str__(self):
        variant_info = f" - {self.variant}" if self.variant else ""
        return f"{self.product.name_ar}{variant_info} ({self.quantity})"
    
    @property
    def unit_price(self):
        """Get the unit price of the item (from variant if available, otherwise from product)"""
        if self.variant and self.variant.price:
            return self.variant.price
        return self.product.price
    
    @property
    def old_unit_price(self):
        """Get the old unit price for calculating discount"""
        return self.product.old_price or self.unit_price
    
    @property
    def total_price(self):
        """Calculate the total price for this item"""
        return self.unit_price * self.quantity
    
    @property
    def discount(self):
        """Calculate the discount for this item"""
        if self.product.old_price and self.product.price < self.product.old_price:
            return (self.product.old_price - self.product.price) * self.quantity
        return 0


class Coupon(models.Model):
    """Coupon model for discounts"""
    code = models.CharField(_("Code"), max_length=50, unique=True)
    description = models.TextField(_("Description"), blank=True)
    discount_value = models.DecimalField(_("Discount Value"), max_digits=10, decimal_places=2)
    is_percentage = models.BooleanField(_("Is Percentage"), default=False)
    minimum_order_value = models.DecimalField(_("Minimum Order Value"), max_digits=10, decimal_places=2, default=0)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    is_active = models.BooleanField(_("Active"), default=True)
    usage_limit = models.PositiveIntegerField(_("Usage Limit"), default=0, help_text=_("0 means unlimited"))
    used_count = models.PositiveIntegerField(_("Used Count"), default=0)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        """Check if the coupon is valid (active, within date range, and not exceeded usage limit)"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
        
        if self.start_date > now or self.end_date < now:
            return False
        
        if self.usage_limit > 0 and self.used_count >= self.usage_limit:
            return False
        
        return True
