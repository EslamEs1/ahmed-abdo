from .models import Category, Collection, Offer

def categories(request):
    """
    Context processor to make categories available across all templates
    """
    return {
        'all_categories': Category.objects.filter(is_active=True, parent=None),
    }

def collections(request):
    """
    Context processor to make active collections available across all templates
    """
    return {
        'active_collections': Collection.objects.filter(is_active=True)[:4],
    }

def offers(request):
    """
    Context processor to make active offers available across all templates
    """
    return {
        'active_offers': Offer.objects.filter(is_active=True)[:2],
    } 