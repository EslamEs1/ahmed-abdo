from django import template
from django.utils.safestring import mark_safe
from apps.contactus.forms import NewsletterForm

register = template.Library()

@register.inclusion_tag('includes/newsletter_form.html')
def render_newsletter_form():
    """Render the newsletter subscription form"""
    return {'newsletter_form': NewsletterForm()} 