from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, Newsletter

class ContactForm(forms.ModelForm):
    """Contact form for the contact page"""
    name = forms.CharField(
        label=_('الاسم'),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('الاسم الكامل')}
        )
    )
    email = forms.EmailField(
        label=_('البريد الإلكتروني'),
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': _('البريد الإلكتروني')}
        )
    )
    phone = forms.CharField(
        label=_('رقم الهاتف'),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('رقم الهاتف')}
        )
    )
    subject = forms.CharField(
        label=_('الموضوع'),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('موضوع الرسالة')}
        )
    )
    message = forms.CharField(
        label=_('الرسالة'),
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': _('رسالتك'), 'rows': 5}
        )
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('أدخل بريدك الإلكتروني'),
                'aria-label': _('البريد الإلكتروني')
            }
        )
    )

    class Meta:
        model = Newsletter
        fields = ['email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError(_('هذا البريد الإلكتروني مشترك بالفعل في النشرة البريدية'))
        return email 