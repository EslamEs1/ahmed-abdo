from django import template
from django.utils.safestring import mark_safe
from ..models import Product, Category, Collection

register = template.Library()

@register.simple_tag
def get_product_image_url(product):
    """
    Returns the main image URL for a product
    """
    main_image = product.images.filter(is_main=True).first()
    if main_image:
        return main_image.image.url
    
    # If no main image, return the first image
    first_image = product.images.first()
    if first_image:
        return first_image.image.url
    
    # If no images, return a placeholder
    return '/static/images/placeholder.jpg'

@register.simple_tag
def get_discount_percentage(product):
    """
    Returns the discount percentage for a product
    """
    if product.old_price and product.price < product.old_price:
        discount = int(((product.old_price - product.price) / product.old_price) * 100)
        return f"{discount}%"
    return ""

@register.simple_tag
def get_filtered_products(category_slug=None, collection_slug=None, limit=None):
    """
    Returns filtered products based on category or collection
    """
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()
        if category:
            products = products.filter(category=category)
    
    if collection_slug:
        collection = Collection.objects.filter(slug=collection_slug).first()
        if collection:
            products = products.filter(collections=collection)
    
    if limit:
        products = products[:int(limit)]
    
    return products

@register.simple_tag
def get_related_products(product, limit=4):
    """
    Returns related products based on the same category
    """
    return Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:limit]

@register.filter
def star_rating(value):
    """
    Converts a numeric rating to HTML star icons
    """
    if not value:
        value = 0
    
    full_stars = int(value)
    half_star = False
    if value - full_stars >= 0.5:
        half_star = True
    
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    
    html = ''
    for i in range(full_stars):
        html += '<i class="bi bi-star-fill"></i>'
    
    if half_star:
        html += '<i class="bi bi-star-half"></i>'
    
    for i in range(empty_stars):
        html += '<i class="bi bi-star"></i>'
    
    return mark_safe(html)

@register.filter
def filter_by_rating(reviews, rating):
    """
    Filter reviews by rating
    """
    return [review for review in reviews if review.rating == int(rating)] 