from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
import uuid

from .models import Cart, CartItem, Coupon
from apps.product.models import Product, ProductVariant
from apps.order.models import Order, OrderItem, ShippingAddress

def _get_or_create_cart(request):
    """Helper function to get or create a cart for the current user/session"""
    if request.user.is_authenticated:
        # Get or create a cart for this user
        cart, created = Cart.objects.get_or_create(
            user=request.user, 
            defaults={'session_id': request.session.session_key or str(uuid.uuid4())}
        )
    else:
        # Get or create a cart for this session
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(
            session_id=session_id,
            defaults={'user': None}
        )
    
    return cart

def cart_view(request):
    """Display the shopping cart"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

@require_POST
def add_to_cart(request):
    """Add a product to the cart"""
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        return JsonResponse({'error': _('Quantity must be at least 1')}, status=400)
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    variant = None
    
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product, is_active=True)
        if variant.stock < quantity:
            return JsonResponse({'error': _('Not enough stock available')}, status=400)
    
    cart = _get_or_create_cart(request)
    
    # Try to get an existing cart item
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product, variant=variant)
        # Update quantity
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        # Create a new cart item
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            variant=variant,
            quantity=quantity
        )
    
    # If variant has stock, decrease it
    if variant and variant.stock >= quantity:
        variant.stock -= quantity
        variant.save()
    
    return JsonResponse({
        'success': True,
        'message': _('Product added to cart'),
        'cart_count': cart.items.count(),
        'cart_total': cart.total_price
    })

@require_POST
def update_cart(request):
    """Update cart item quantity"""
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        return JsonResponse({'error': _('Quantity must be at least 1')}, status=400)
    
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Check stock if there's a variant
    if cart_item.variant:
        available_stock = cart_item.variant.stock + cart_item.quantity  # Current stock + what's already in cart
        if available_stock < quantity:
            return JsonResponse({'error': _('Not enough stock available')}, status=400)
    
    # Update variant stock
    if cart_item.variant:
        # Add the current quantity back to stock
        cart_item.variant.stock += cart_item.quantity
        # Subtract the new quantity from stock
        cart_item.variant.stock -= quantity
        cart_item.variant.save()
    
    # Update cart item quantity
    cart_item.quantity = quantity
    cart_item.save()
    
    return JsonResponse({
        'success': True,
        'item_total': cart_item.total_price,
        'cart_total': cart.total_price,
        'cart_discount': cart.total_discount,
        'cart_final': cart.final_price
    })

@require_POST
def remove_from_cart(request):
    """Remove an item from the cart"""
    item_id = request.POST.get('item_id')
    
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Return stock to variant if needed
    if cart_item.variant:
        cart_item.variant.stock += cart_item.quantity
        cart_item.variant.save()
    
    # Delete the cart item
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'message': _('Item removed from cart'),
        'cart_count': cart.items.count(),
        'cart_total': cart.total_price,
        'cart_discount': cart.total_discount,
        'cart_final': cart.final_price
    })

@require_POST
def apply_coupon(request):
    """Apply a coupon code to the cart"""
    coupon_code = request.POST.get('coupon_code', '').strip().upper()
    
    if not coupon_code:
        return JsonResponse({'error': _('Please enter a coupon code')}, status=400)
    
    try:
        coupon = Coupon.objects.get(code=coupon_code, is_active=True)
    except Coupon.DoesNotExist:
        return JsonResponse({'error': _('Invalid coupon code')}, status=400)
    
    # Check if coupon is valid
    if not coupon.is_valid:
        return JsonResponse({'error': _('This coupon has expired or reached its usage limit')}, status=400)
    
    cart = _get_or_create_cart(request)
    
    # Check minimum order value
    if cart.total_price < coupon.minimum_order_value:
        return JsonResponse({
            'error': _('This coupon requires a minimum order of {0}').format(coupon.minimum_order_value)
        }, status=400)
    
    # Calculate discount
    if coupon.is_percentage:
        discount = (coupon.discount_value / 100) * cart.total_price
    else:
        discount = min(coupon.discount_value, cart.total_price)  # Can't discount more than the cart total
    
    # Store coupon in session for later use when creating the order
    request.session['coupon_id'] = coupon.id
    request.session['coupon_discount'] = float(discount)
    
    return JsonResponse({
        'success': True,
        'message': _('Coupon applied successfully'),
        'discount': discount,
        'cart_final': cart.total_price - discount
    })

@require_POST
def clear_cart(request):
    """Clear all items from the cart"""
    cart = _get_or_create_cart(request)
    
    # Return stock to variants
    for item in cart.items.all():
        if item.variant:
            item.variant.stock += item.quantity
            item.variant.save()
    
    # Delete all cart items
    cart.items.all().delete()
    
    return JsonResponse({
        'success': True,
        'message': _('Cart cleared')
    })

def checkout_view(request):
    """Display the checkout page"""
    cart = _get_or_create_cart(request)
    
    # Redirect to cart if empty
    if cart.items.count() == 0:
        messages.warning(request, _('Your cart is empty'))
        return redirect('cart:cart')
    
    # Get saved addresses if user is logged in
    addresses = []
    if request.user.is_authenticated:
        addresses = ShippingAddress.objects.filter(user=request.user)
    
    # Get coupon from session if exists
    coupon_discount = 0
    coupon = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon_discount = request.session.get('coupon_discount', 0)
        except Coupon.DoesNotExist:
            pass
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'addresses': addresses,
        'coupon': coupon,
        'coupon_discount': coupon_discount,
        'final_price': cart.total_price - coupon_discount
    }
    
    return render(request, 'checkout.html', context)
