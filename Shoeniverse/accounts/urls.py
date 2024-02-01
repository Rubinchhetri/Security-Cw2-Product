from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # User Related Views
    path('userLogin', views.userLogin, name='userLogin'),
    path('userRegister', views.userRegister, name='userRegister'),
    path('logout', views.logout, name='logout'),
    path('userDashboard', views.userDashboard, name='userDashboard'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    

    # Important Function Defined
    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    # Admin Related Views
    path('adminDashboard', views.adminDashboard, name='adminDashboard'),
    path('logoutadmin', views.logoutadmin, name='logoutadmin'),

    path('admin-products', views.admin_products_view, name='admin-products'),
    path('admin-add-product', views.admin_add_product_view, name='admin-add-product'),
    path('delete-product/<int:pk>',views.delete_product_view, name='delete-product'),
    path('update-product/<int:pk>',views.update_product_view, name='update-product'),

    path('admin-view-booking', views.admin_view_booking_view, name='admin-view-booking'),
    path('update-order/<int:pk>', views.update_order_view, name='update-order'),
    path('delete-order/<int:pk>', views.delete_order_view, name='delete-order'),

    path('view-customer', views.view_customer, name='view-customer'),
    path('delete-customer/<int:pk>',views.delete_customer_view, name='delete-customer'),

    # User Related Views
    path('edit-profile', views.edit_profile_view, name='edit-profile'),
    path('deleteuser/<int:user_id>', views.delete_user, name='deleteuser'),
    path('my-order/<int:id>', views.my_order_view, name='my-order'),
]
