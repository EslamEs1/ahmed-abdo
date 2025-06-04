from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # Category pages
    path('men/', views.men_category, name='men_category'),
    path('women/', views.women_category, name='women_category'),
    path('kids/', views.kids_category, name='kids_category'),
    
    # Product detail
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Offers page
    path('offers/', views.offers_list, name='offers_list'),
    
    # Collection detail
    path('collection/', views.collection, name='collection'),
    
    # Add review
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    
    # Category list (generic)
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),
]