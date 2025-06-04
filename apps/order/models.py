from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.product.models import Product, ProductVariant
from apps.cart.models import Coupon

class Order(models.Model):
    """Order model for customer purchases"""
    ORDER_STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('fawry', _('Fawry')),
        ('vodafone_cash', _('Vodafone Cash')),
        ('etisalat_cash', _('Etisalat Cash')),
        ('instapay', _('InstaPay')),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                             related_name='orders', verbose_name=_("User"))
    order_number = models.CharField(_("Order Number"), max_length=20, unique=True)
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20)
    address = models.TextField(_("Address"))
    city = models.CharField(_("City"), max_length=100)
    area = models.CharField(_("Area"), max_length=100)
    order_note = models.TextField(_("Order Note"), blank=True, null=True)
    order_total = models.DecimalField(_("Order Total"), max_digits=10, decimal_places=2)
    discount = models.DecimalField(_("Discount"), max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, 
                              related_name='orders', verbose_name=_("Coupon"))
    shipping_cost = models.DecimalField(_("Shipping Cost"), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_("Order Status"), max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(_("Payment Method"), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(_("Payment Status"), max_length=20, 
                                     choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_reference = models.CharField(_("Payment Reference"), max_length=200, blank=True, null=True)
    payment_screenshot = models.ImageField(_("Payment Screenshot"), upload_to='payment_screenshots/', blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("IP Address"), blank=True, null=True)
    is_ordered = models.BooleanField(_("Is Ordered"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_number
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_price(self):
        """Calculate the total price of all items in the order"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def final_price(self):
        """Calculate the final price after discount and shipping"""
        return self.total_price - self.discount + self.shipping_cost


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, blank=True, null=True, 
                              verbose_name=_("Variant"))
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    old_price = models.DecimalField(_("Old Price"), max_digits=10, decimal_places=2, blank=True, null=True)
    color = models.CharField(_("Color"), max_length=50, blank=True, null=True)
    size = models.CharField(_("Size"), max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
    
    def __str__(self):
        return f"{self.product.name_ar} ({self.quantity})"
    
    @property
    def total_price(self):
        """Calculate the total price for this item"""
        return self.price * self.quantity
    
    @property
    def discount(self):
        """Calculate the discount for this item"""
        if self.old_price and self.price < self.old_price:
            return (self.old_price - self.price) * self.quantity
        return 0


class ShippingAddress(models.Model):
    """Shipping address model for saved addresses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_("User"))
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20)
    address = models.TextField(_("Address"))
    city = models.CharField(_("City"), max_length=100)
    area = models.CharField(_("Area"), max_length=100)
    is_default = models.BooleanField(_("Default Address"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.area}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set other addresses of this user as non-default
            ShippingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class OrderTracker(models.Model):
    """Order tracking model for order status updates"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking', verbose_name=_("Order"))
    status = models.CharField(_("Status"), max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Order Tracker")
        verbose_name_plural = _("Order Trackers")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"
