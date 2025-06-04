from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product, ProductVariant, ProductImage

@receiver(post_save, sender=Product)
def create_default_variant(sender, instance, created, **kwargs):
    """
    Create a default variant when a product is created
    """
    if created:
        # Check if there are any variants already
        if not ProductVariant.objects.filter(product=instance).exists():
            # Get the first size and color or create them if none exist
            from .models import Size, Color
            
            size = Size.objects.first()
            if not size:
                size = Size.objects.create(name='Default', name_ar='افتراضي')
                
            color = Color.objects.first()
            if not color:
                color = Color.objects.create(name='Default', name_ar='افتراضي', code='#000000')
            
            # Create default variant
            ProductVariant.objects.create(
                product=instance,
                size=size,
                color=color,
                sku=f"{instance.id}-default",
                price=instance.price,
                stock=10,
                is_active=True
            )

@receiver(pre_save, sender=Product)
def update_sale_status(sender, instance, **kwargs):
    """
    Update is_on_sale status based on old_price
    """
    if instance.old_price and instance.price < instance.old_price:
        instance.is_on_sale = True
    else:
        instance.is_on_sale = False

@receiver(post_save, sender=ProductImage)
def ensure_one_main_image(sender, instance, created, **kwargs):
    """
    Ensure only one image is set as main for a product
    """
    if instance.is_main:
        # Set all other images as not main
        ProductImage.objects.filter(
            product=instance.product, 
            is_main=True
        ).exclude(id=instance.id).update(is_main=False)
    else:
        # If no main image exists, set the first one as main
        if not ProductImage.objects.filter(product=instance.product, is_main=True).exists():
            first_image = ProductImage.objects.filter(product=instance.product).first()
            if first_image:
                first_image.is_main = True
                first_image.save() 