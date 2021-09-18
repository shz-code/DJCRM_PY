from django.urls import path
from . import views

app_name= 'accounts'

urlpatterns = [
    path('', views.home , name='home'),
    path('products/', views.products , name='products'),
    path('create-order/', views.createOrder , name='create_order'),
    path('update-order/<int:pk>', views.updateOrder , name='update_order'),
    path('delete_order/<int:pk>', views.deleteOrder , name='delete_order'),
    path('customer/<int:pk>', views.customer , name='customer'),
    path('create-customer/', views.createCustomer , name='create_customer'),
    path('update-customer/<int:pk>', views.updateCustomer , name='update_customer'),
    path('delete-customer/<int:pk>', views.deleteCustomer , name='delete_customer'),
]
