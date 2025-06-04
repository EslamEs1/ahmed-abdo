from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone

from .models import Order, OrderItem, ShippingAddress, OrderTracker
from apps.cart.models import Cart, CartItem, Coupon
from apps.product.models import Product, ProductVariant

def generate_order_number():
    """Generate a unique order number"""
    # Format: YYMMDDxxxx where xxxx is a random string
    timestamp = timezone.now().strftime('%y%m%d')
    random_str = get_random_string(length=4, allowed_chars='0123456789')
    return f"{timestamp}{random_str}"

@login_required
def create_address(request):
    """Create a new shipping address"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        area = request.POST.get('area')
        is_default = request.POST.get('is_default', False) == 'on'
        
        # Create a new address
        ShippingAddress.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            area=area,
            is_default=is_default
        )
        
        messages.success(request, _('Address saved successfully'))
        return redirect('cart:checkout')
    
    # If GET request, redirect to checkout
    return redirect('cart:checkout')

@require_POST
def place_order(request):
    """Place an order"""
    # Get cart
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        session_id = request.session.session_key
        cart = get_object_or_404(Cart, session_id=session_id)
    
    # Check if cart is empty
    if cart.items.count() == 0:
        messages.warning(request, _('Your cart is empty'))
        return redirect('cart:cart')
    
    # Get form data
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    area = request.POST.get('area')
    order_note = request.POST.get('order_note')
    payment_method = request.POST.get('payment_method')
    
    # Save address if requested (for logged in users)
    if request.user.is_authenticated and request.POST.get('save_address'):
        is_default = request.POST.get('is_default') == 'on'
        ShippingAddress.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            area=area,
            is_default=is_default
        )
    
    # Get coupon from session
    coupon = None
    discount = 0
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            discount = request.session.get('coupon_discount', 0)
        except Coupon.DoesNotExist:
            pass
    
    # Calculate shipping cost (free for orders over 500)
    shipping_cost = 0 if cart.total_price >= 500 else 50
    
    # Create order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        order_number=generate_order_number(),
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        area=area,
        order_note=order_note,
        order_total=cart.total_price,
        discount=discount,
        coupon=coupon,
        shipping_cost=shipping_cost,
        payment_method=payment_method,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            variant=cart_item.variant,
            quantity=cart_item.quantity,
            price=cart_item.unit_price,
            old_price=cart_item.old_unit_price,
            color=cart_item.variant.color.name_ar if cart_item.variant and hasattr(cart_item.variant, 'color') else None,
            size=cart_item.variant.size.name_ar if cart_item.variant and hasattr(cart_item.variant, 'size') else None
        )
    
    # Create order tracker entry
    OrderTracker.objects.create(
        order=order,
        status='pending',
        description=_('Order placed successfully')
    )
    
    # Increment coupon usage if used
    if coupon:
        coupon.used_count += 1
        coupon.save()
    
    # Clear cart
    cart.items.all().delete()
    
    # Clear session data
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    
    # Save order id in session
    request.session['order_id'] = order.id
    
    # Redirect to payment page or order confirmation
    if payment_method in ['fawry', 'vodafone_cash', 'etisalat_cash', 'instapay']:
        return redirect('order:payment', order_number=order.order_number)
    else:
        return redirect('order:order_complete')

def payment_view(request, order_number):
    """Display payment information for an order"""
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order
    }
    
    return render(request, 'order/payment.html', context)

@require_POST
def upload_payment_proof(request, order_number):
    """Upload payment proof for an order"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if 'payment_screenshot' in request.FILES:
        order.payment_screenshot = request.FILES['payment_screenshot']
        order.payment_status = 'processing'
        order.save()
        
        # Create order tracker entry
        OrderTracker.objects.create(
            order=order,
            status='processing',
            description=_('Payment proof uploaded, waiting for confirmation')
        )
        
        messages.success(request, _('Payment proof uploaded successfully'))
    else:
        messages.error(request, _('Please upload a payment screenshot'))
    
    return redirect('order:order_complete')

def order_complete(request):
    """Display order completion page"""
    order_id = request.session.get('order_id')
    
    if order_id:
        order = Order.objects.get(id=order_id)
        
        context = {
            'order': order,
            'order_items': order.items.all()
        }
        
        # Clear session
        if 'order_id' in request.session:
            del request.session['order_id']
        
        return render(request, 'order/order_complete.html', context)
    else:
        # If no order in session, redirect to home
        return redirect('main:home')

@login_required
def order_history(request):
    """Display order history for logged in users"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    
    return render(request, 'order/order_history.html', context)

@login_required
def order_detail(request, order_number):
    """Display order details for a specific order"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_items = order.items.all()
    order_tracking = order.tracking.all().order_by('-created_at')
    
    context = {
        'order': order,
        'order_items': order_items,
        'order_tracking': order_tracking
    }
    
    return render(request, 'order/order_detail.html', context)
