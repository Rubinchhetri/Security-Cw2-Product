from django.contrib import admin
from .models import Cart, CartItem, Orders

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "date_added",)

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "is_active")

admin.site.register(CartItem, CartItemAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "status")
    list_editable = ("status",)

admin.site.register(Orders, OrdersAdmin)



