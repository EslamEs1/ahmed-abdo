from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ContactMessage, ContactInfo
from .forms import ContactForm

def contact_view(request):
    """View for displaying contact page with form and contact information"""
    # Get active contact info
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    # Initialize empty form
    form = ContactForm()
    
    context = {
        'contact_info': contact_info,
        'form': form,
    }
    
    return render(request, 'contactus.html', context)

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
