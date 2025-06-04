from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from .models import Product, Category, Collection, Offer, Review, ProductVariant



def category_list(request, category_slug=None):
    """
    View for displaying products by category (men, women, kids)
    """
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        # For subcategories, filter by the specific category
        if category.parent:
            products = products.filter(category=category)
        # For main categories, include products from all subcategories
        else:
            subcategories = category.children.all()
            products = products.filter(category__in=list(subcategories) + [category])
    
    # Handle sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.annotate(review_count=Count('reviews')).order_by('-review_count')
    else:  # Default: newest
        products = products.order_by('-created_at')
    
    # Pagination
    per_page = request.GET.get('per_page', 24)
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Determine which template to use based on category
    template_name = None
    
    # Check if it's a main category or subcategory
    if category:
        if category.parent is None:
            # Main category
            if category.slug == 'men':
                template_name = 'men.html'
            elif category.slug == 'women':
                template_name = 'women.html'
            elif category.slug == 'kids':
                template_name = 'kids.html'
        else:
            # Subcategory - use the parent's template
            if category.parent.slug == 'men':
                template_name = 'men.html'
            elif category.parent.slug == 'women':
                template_name = 'women.html'
            elif category.parent.slug == 'kids':
                template_name = 'kids.html'
            else:
                template_name = 'men.html'  # Default fallback
    
    if not template_name:
        template_name = 'men.html'  # Default fallback
    
    context = {
        'category': category,
        'categories': categories,
        'products': page_obj,
        'sort_by': sort_by,
        'page_obj': page_obj,
    }
    
    return render(request, template_name, context)

def men_category(request):
    """View for men's category page"""
    category = get_object_or_404(Category, slug='men', is_active=True)
    return category_list(request, category.slug)

def women_category(request):
    """View for women's category page"""
    category = get_object_or_404(Category, slug='women', is_active=True)
    return category_list(request, category.slug)

def kids_category(request):
    """View for kids' category page"""
    category = get_object_or_404(Category, slug='kids', is_active=True)
    return category_list(request, category.slug)

def product_detail(request, slug):
    """
    View for product detail page
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get product variants
    variants = ProductVariant.objects.filter(product=product, is_active=True)
    
    # Get available sizes and colors
    sizes = set(variant.size for variant in variants)
    colors = set(variant.color for variant in variants)
    
    # Get product images
    images = product.images.all()
    
    # Get product reviews
    reviews = product.reviews.filter(is_approved=True)
    review_count = reviews.count()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'variants': variants,
        'sizes': sizes,
        'colors': colors,
        'images': images,
        'reviews': reviews,
        'review_count': review_count,
        'avg_rating': avg_rating,
        'related_products': related_products,
    }
    
    return render(request, 'product.html', context)

def offers_list(request):
    """
    View for offers page
    """
    # Filter offers to only include those with images
    active_offers = Offer.objects.filter(is_active=True).exclude(image='')
    
    # Get products with offers/discounts
    products_with_offers = Product.objects.filter(
        is_active=True, 
        is_on_sale=True
    )
    
    # Handle sorting
    sort_by = request.GET.get('sort', 'discount')
    if sort_by == 'price_low':
        products_with_offers = products_with_offers.order_by('price')
    elif sort_by == 'price_high':
        products_with_offers = products_with_offers.order_by('-price')
    elif sort_by == 'popular':
        products_with_offers = products_with_offers.annotate(review_count=Count('reviews')).order_by('-review_count')
    elif sort_by == 'discount':
        # Sort by discount percentage (highest to lowest)
        # This uses a calculated field so we need to annotate
        products_with_offers = sorted(
            products_with_offers,
            key=lambda p: p.get_discount_percentage() if p.get_discount_percentage() else 0,
            reverse=True
        )
    else:  # Default: newest
        products_with_offers = products_with_offers.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products_with_offers, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'offers': active_offers,
        'products': page_obj,
        'page_obj': page_obj,
        'sort_by': sort_by,
    }
    
    return render(request, 'offers.html', context)

def collection(request):
    """
    View for collection detail page
    """
    collection = Collection.objects.filter(is_active=True).last()
    products = collection.products.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'collection': collection,
        'products': page_obj,
        'page_obj': page_obj,
    }
    
    return render(request, 'collection.html', context)

def add_review(request, product_id):
    """
    View for adding product reviews
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if name and email and rating and comment:
            Review.objects.create(
                product=product,
                name=name,
                email=email,
                rating=rating,
                comment=comment,
                is_approved=False  # Reviews need approval before being displayed
            )
            # Add success message
    
    # Redirect back to product detail page
    return redirect('product:product_detail', slug=product.slug)