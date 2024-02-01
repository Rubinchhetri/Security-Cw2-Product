from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.activity_logger import log_activity
from .models import Cart, CartItem, Product, Orders


# Create your views here.

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id
    
@login_required(login_url='userLogin')
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            messages.success(request, "Item Already In Cart")
            return redirect('store')
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                user=current_user,
            )
            cart_item.save()
            messages.success(request, "Item Added In Cart")
            log_activity(current_user, f'Add to cart')

        return redirect('store')

@login_required(login_url='userLogin')
def cart(request, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)
    except:
        # print("except")
        pass

    context = {
        "cart_items": cart_items,
    }

    return render(request, 'store/cart.html', context)

@login_required(login_url='userLogin')
def remove_cart_item(request, cart_item_id):
    current_user = request.user
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    messages.success(request, "Item Sucessfully Removed")
    log_activity(current_user, f'Delete Cart Item')
    return redirect('cart')

@login_required(login_url='userLogin')
def payment(request):
    return render(request, 'store/payment.html')


@login_required(login_url='userLogin')
def completeOrder(request):
    current_user = request.user
    log_activity(current_user, f'Order Item')
    return render(request, 'store/ordercomplete.html')

@login_required(login_url='userLogin')
def purchaseitem(request, product_id):
    if request.method == "POST":
        current_user = request.user
        product = Product.objects.get(id=product_id)
        
        order = Orders(user=current_user, product=product)
        order.save()

        cart_item_id  = request.POST['cart_item_id']
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()

        messages.success(request, "Item Ordered")
        return redirect('payment')