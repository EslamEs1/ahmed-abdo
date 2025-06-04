from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Form for contact page"""
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your Name')}),
        max_length=100
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your Email')}),
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Subject')}),
        max_length=200
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Your Message'), 'rows': 5}),
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message'] 