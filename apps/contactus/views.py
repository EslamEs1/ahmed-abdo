from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ContactMessage, ContactInfo
from .forms import ContactForm, NewsletterForm

def contact_view(request):
    """View for the contact page"""
    contact_info = ContactInfo.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم إرسال رسالتك بنجاح. سنتواصل معك قريبًا.'))
            return redirect(reverse('contactus:contact'))
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'contact_info': contact_info,
        'newsletter_form': NewsletterForm(),
    }
    
    return render(request, 'contactus/contact.html', context)

@require_POST
def submit_contact(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX request
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Create contact message
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            return JsonResponse({
                'success': True,
                'message': _('شكرا لك على رسالتك. سنتواصل معك قريباً.')
            })
        else:
            # Handle regular form submission
            form = ContactForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, _('شكرا لك على رسالتك. سنتواصل معك قريباً.'))
                return redirect('contactus:contact')
            else:
                messages.error(request, _('يرجى التصحيح الأخطاء أدناه.'))
                return render(request, 'contactus.html', {'form': form, 'contact_info': ContactInfo.objects.filter(is_active=True).first()})

@require_POST
def newsletter_subscribe(request):
    """Handle newsletter subscription via AJAX or regular form submission"""
    form = NewsletterForm(request.POST)
    
    if form.is_valid():
        form.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': _('شكراً لاشتراكك في النشرة البريدية!')
            })
        else:
            messages.success(request, _('شكراً لاشتراكك في النشرة البريدية!'))
            # Redirect back to the referring page
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': form.errors.get('email', _('حدث خطأ أثناء الاشتراك. يرجى المحاولة مرة أخرى.'))
            })
        else:
            messages.error(request, form.errors.get('email', _('حدث خطأ أثناء الاشتراك. يرجى المحاولة مرة أخرى.')))
            # Redirect back to the referring page
            return redirect(request.META.get('HTTP_REFERER', '/'))
