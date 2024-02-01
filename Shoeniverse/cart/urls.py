from django.urls import path
from cart import views


urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_cart, name="add-to-cart"),
    path('remove_item/<int:cart_item_id>/', views.remove_cart_item, name="remove_item"),
    
    path('purchaseitem/<int:product_id>/', views.purchaseitem, name="purchaseitem"),
    path('payment', views.payment, name='payment'),
    path('completeOrder', views.completeOrder, name='completeOrder'),
    
]
