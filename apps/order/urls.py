from django.urls import path
from .views import (
    create_address,
    place_order,
    payment_view,
    upload_payment_proof,
    order_complete,
    order_history,
    order_detail
)

app_name = "order"
urlpatterns = [
    path('create-address/', create_address, name='create_address'),
    path('place-order/', place_order, name='place_order'),
    path('payment/<str:order_number>/', payment_view, name='payment'),
    path('upload-payment/<str:order_number>/', upload_payment_proof, name='upload_payment'),
    path('complete/', order_complete, name='order_complete'),
    path('history/', order_history, name='order_history'),
    path('detail/<str:order_number>/', order_detail, name='order_detail'),
]