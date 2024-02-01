from django.test import TestCase
from django.urls import reverse,resolve
from django.test import Client, SimpleTestCase, TestCase
from accounts.views import userLogin, userRegister, logout, userDashboard, adminDashboard, logoutadmin, delete_user, edit_profile_view, afterlogin_view
from accounts.views import admin_products_view, admin_add_product_view, delete_product_view, update_product_view, admin_view_booking_view
from accounts.views import update_order_view, delete_order_view, view_customer, delete_customer_view, my_order_view

from cart.views import cart, add_cart, remove_cart_item, purchaseitem, payment, completeOrder

from ecom.views import home, about, contact

from store.views import store

# Create your tests here.
class TestUrls(SimpleTestCase):
    def test_case_register_url(self):
        url=reverse("userRegister")
        print(resolve(url))
        self.assertEquals(resolve(url).func,userRegister)

    def test_case_login_url(self):
        url=reverse("userLogin")
        print(resolve(url))
        self.assertEquals(resolve(url).func,userLogin)
    
    def test_case_logout_url(self):
        url=reverse("logout")
        print(resolve(url))
        self.assertEquals(resolve(url).func,logout)

    def test_case_home_url(self):
        url=reverse("userDashboard")
        print(resolve(url))
        self.assertEquals(resolve(url).func,userDashboard)
    
    def test_case_dashboard_url(self):
        url=reverse("adminDashboard")
        print(resolve(url))
        self.assertEquals(resolve(url).func,adminDashboard)


    def test_case_delete_user_url(self):
        url=reverse("deleteuser", args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_user)

    
    def test_case_gallery_url(self):
        url=reverse("logoutadmin")
        print(resolve(url))
        self.assertEquals(resolve(url).func,logoutadmin)
    

    def test_case_afterlogin_view_url(self):
        url=reverse("edit-profile")
        print(resolve(url))
        self.assertEquals(resolve(url).func,edit_profile_view)
    
    def test_case_edit_profile_view_url(self):
        url=reverse("afterlogin")
        print(resolve(url))
        self.assertEquals(resolve(url).func,afterlogin_view)
    
    def test_case_admin_products_view_url(self):
        url=reverse("admin-products")
        print(resolve(url))
        self.assertEquals(resolve(url).func,admin_products_view)
    
    def test_case_admin_add_product_view_url(self):
        url=reverse("admin-add-product")
        print(resolve(url))
        self.assertEquals(resolve(url).func,admin_add_product_view)
    
    def test_case_delete_product_view_url(self):
        url=reverse("delete-product", args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_product_view)
    
    def test_case_update_product_view_url(self):
        url=reverse("update-product", args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,update_product_view)

    def test_case_admin_view_booking_view_url(self):
        url=reverse("admin-view-booking")
        print(resolve(url))
        self.assertEquals(resolve(url).func,admin_view_booking_view)
    
    def test_case_update_order_view_url(self):
        url=reverse("update-order", args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,update_order_view)
    
    def test_case_delete_order_view_url(self):
        url=reverse("delete-order", args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_order_view)
    
    def test_case_view_customer_view_url(self):
        url=reverse("view-customer")
        print(resolve(url))
        self.assertEquals(resolve(url).func,view_customer)
    
    def test_case_delete_customer_view_url(self):
        url=reverse("delete-customer" , args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_customer_view)

    def test_case_my_order_view_url(self):
        url=reverse("my-order" , args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,my_order_view)

    # Test cases from cart
    def test_case_cart_view_url(self):
        url=reverse("cart")
        print(resolve(url))
        self.assertEquals(resolve(url).func,cart)
    
    def test_case_add_cart_view_url(self):
        url=reverse("add-to-cart" , args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,add_cart)
    
    def test_case_remove_cart_item_view_url(self):
        url=reverse("remove_item" , args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,remove_cart_item)
    
    def test_case_purchaseitem_view_url(self):
        url=reverse("purchaseitem" , args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func,purchaseitem)
    
    def test_case_payment_view_url(self):
        url=reverse("payment")
        print(resolve(url))
        self.assertEquals(resolve(url).func,payment)
    
    def test_case_completeOrder_view_url(self):
        url=reverse("completeOrder")
        print(resolve(url))
        self.assertEquals(resolve(url).func,completeOrder)
    
    # Test Cases from Ecom
    def test_case_home_page_url(self):
        url=reverse("home")
        print(resolve(url))
        self.assertEquals(resolve(url).func,home)
    
    def test_case_contact_url(self):
        url=reverse("contact")
        print(resolve(url))
        self.assertEquals(resolve(url).func,contact)

    def test_case_about_url(self):
        url=reverse("about")
        print(resolve(url))
        self.assertEquals(resolve(url).func,about)
    
    def test_case_store_url(self):
        url=reverse("store")
        print(resolve(url))
        self.assertEquals(resolve(url).func,store)


# Test Cases for views
class TestViews(TestCase):
    def setUp(self):
        self.client=Client()
    
    def test_store_views(self):
        response=self.client.get(reverse('store'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'store/store.html')
    
    def test_about_views(self):
        response=self.client.get(reverse('about'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'pages/about.html')
    
    def test_userLogin_views(self):
        response=self.client.get(reverse('userLogin'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/userLogin.html')
    
    def test_userRegister_views(self):
        response=self.client.get(reverse('userRegister'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/userRegister.html')
    
    
