from django.shortcuts import render
from apps.product.models import Product, Category, Collection, Offer

# Create your views here.


def home(request):
    # Get featured products
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    
    # Get main categories (men, women, kids)
    main_categories = Category.objects.filter(parent=None, is_active=True)
    
    # Get active collections
    active_collections = Collection.objects.filter(is_active=True)[:2]
    
    # Get active offers
    active_offers = Offer.objects.filter(is_active=True)[:2]
    
    context = {
        'featured_products': featured_products,
        'main_categories': main_categories,
        'collections': active_collections,
        'offers': active_offers,
    }
    
    return render(request, 'index.html', context)