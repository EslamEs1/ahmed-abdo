from django import template
from django.utils.safestring import mark_safe
from apps.main.models import Slider

register = template.Library()

@register.simple_tag
def get_sliders(page_type):
    """Get sliders for a specific page type"""
    return Slider.objects.filter(page=page_type, is_active=True).order_by('order')

@register.inclusion_tag('includes/slider_home_page.html')
def render_home_slider():
    """Render the home page slider"""
    sliders = Slider.objects.filter(page='home', is_active=True).order_by('order')
    return {'sliders': sliders}

@register.inclusion_tag('includes/slider_product_page.html')
def render_product_slider(page_type):
    """Render the product page slider with the specified page type"""
    sliders = Slider.objects.filter(page=page_type, is_active=True).order_by('order')
    return {'sliders': sliders, 'page_type': page_type} 