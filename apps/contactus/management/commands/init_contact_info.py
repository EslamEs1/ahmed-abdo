from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from apps.contactus.models import ContactInfo

class Command(BaseCommand):
    help = 'Initialize contact information for the website'

    def handle(self, *args, **options):
        if ContactInfo.objects.exists():
            self.stdout.write(self.style.WARNING('Contact information already exists.'))
            
            # Ask if user wants to override
            answer = input("Do you want to update the existing contact info? (y/n): ")
            if answer.lower() != 'y':
                self.stdout.write(self.style.SUCCESS('Operation cancelled.'))
                return
            
            # Update existing contact info
            contact_info = ContactInfo.objects.filter(is_active=True).first()
            if not contact_info:
                contact_info = ContactInfo.objects.first()
        else:
            # Create new contact info
            contact_info = ContactInfo()
        
        # Set values
        contact_info.address = 'شارع التحرير، القاهرة، مصر'
        contact_info.phone = '+20 123 456 7890'
        contact_info.email = 'info@ahmedabdo.com'
        contact_info.map_url = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3418.0940461667!2d31.235774!3d30.044420!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzDCsDAyJzM5LjkiTiAzMcKwMTQnMDguOCJF!5e0!3m2!1sen!2seg!4v1635959877964!5m2!1sen!2seg'
        contact_info.is_active = True
        contact_info.save()
        
        self.stdout.write(self.style.SUCCESS('Contact information initialized successfully!')) 