from django.urls import path
from .views import contact_view, submit_contact

app_name = "contactus"
urlpatterns = [
    path('', contact_view, name='contact'),
    path('submit/', submit_contact, name='submit_contact'),
]