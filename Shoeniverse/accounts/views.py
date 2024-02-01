from django.shortcuts import render, redirect
from . import forms, models
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from cart.models import Orders
from cart import forms
from accounts.forms import UserForm, ProductForm
from django.core.paginator import Paginator

# Create your views here.
from django.core.cache import cache
from accounts.activity_logger import log_activity
from datetime import datetime, timedelta
import re
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.password_validation import (
    validate_password,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError

MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 minutes in seconds
SESSION_EXPIRY_MINUTES = 1


def userLogin(request):
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        lockout_key = f'lockout_{username}'
        if cache.get(lockout_key):
            error_message = "Your account is locked. Please try again later."
            messages.error(request, error_message)
            context = {'users': users, 'error_message': error_message}
            # return render(request, "login.html", context)
            return render(request, 'accounts/userLogin.html', context)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            customer = user.get_username

            log_activity(user, f'Logged in')
            # messages.success(request, 'You are now logged in.')

            # Reset login attempts
            cache.delete(lockout_key)

            # Set session expiry
            request.session.set_expiry(
                int(timedelta(minutes=SESSION_EXPIRY_MINUTES).total_seconds()))

            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")

            # Increment failed login attempts
            increment_login_attempts(username)

        # Check if the user has reached the maximum login attempts
            if get_login_attempts(username) >= MAX_LOGIN_ATTEMPTS:
                cache.set(lockout_key, True, LOCKOUT_DURATION)
                # error_message = "Your account is locked. Please try again later."
                messages.error(request, "account is locked")
            else:
                error_message = "Invalid username or password."

            # context = {'users': users, 'error_message': error_message}

            return redirect('userLogin')
    return render(request, 'accounts/userLogin.html')


def increment_login_attempts(username):
    attempts_key = f'login_attempts_{username}'
    attempts = cache.get(attempts_key)

    if attempts is None:
        cache.set(attempts_key, 1, LOCKOUT_DURATION)
    else:
        cache.incr(attempts_key)


def get_login_attempts(username):
    attempts_key = f'login_attempts_{username}'
    attempts = cache.get(attempts_key)

    if attempts is None:
        attempts = 0

    return attempts

# def userRegister(request):
#     customer_form = UserForm()
#     is_registered = False  # Flag to track registration completion
#     if request.method == 'POST':
#         customer_form = UserForm(request.POST)
#         if customer_form.is_valid():
#             username = request.POST['username']
#             firstname = request.POST['firstname']
#             lastname = request.POST['lastname']
#             email = request.POST['email']
#             password = request.POST['password']
#             confirm_password = request.POST['confirm_password']
#             if password == confirm_password:
#                 # Check if the password contains personal information
#                 if contains_personal_info(username, password):
#                     error_message = "Passwords should not include personal information."
#                     messages.error(request, error_message)
#                 else:
#                     if User.objects.filter(username=username).exists():
#                         messages.error(request, 'Username already exists')
#                         # return redirect('userRegister')
#                     else:
#                         try:
#                             validate_password(
#                                 password=password,
#                                 user=User,
#                                 password_validators=[
#                                     CommonPasswordValidator(),  # Prevent common passwords
#                                     NumericPasswordValidator(),  # Require at least one digit
#                                 ],
#                             )
#                             if len(password) < 8 or len(password) > 12:
#                                 raise ValidationError('Password must be 8-12 characters long.')
#                             if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', password):
#                                 raise ValidationError('Password must include uppercase and lowercase letters, numbers, and special characters.')
#                         except ValidationError as e:
#                             messages.error(request, ', '.join(e.messages))

#                         if User.objects.filter(email=email).exists():
#                             messages.error(request, 'Email already exists')
#                             # return redirect('userRegister')
#                         else:
#                             user = User.objects.create_user(
#                                 first_name=firstname, last_name=lastname, email=email, username=username, password=password)
#                             auth.login(request, user)
#                             user.save()
#                             customer = customer_form.save(commit=False)
#                             customer.save()
#                             messages.success(
#                                 request, 'You are registered successfully')
#                             log_activity(user, f'Registered into the system')
#                             # return redirect('userRegister')
#                             return HttpResponseRedirect('userRegister')

#             else:
#                 messages.error(request, 'Password do not match')
#                 # return redirect('userRegister')
#                 return HttpResponseRedirect('userRegister')
#     else:
#         return render(request, 'accounts/userRegister.html')


def contains_personal_info(username, password):
    # Perform personal information check, e.g., using regular expressions
    # You can customize this function based on your specific requirements
    personal_info_patterns = [
        r"\b" + re.escape(username) + r"\b",  # Check for username
        # Check for date of birth in format YYYY-MM-DD
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{10}\b"  # Check for phone number with 10 digits
    ]
    for pattern in personal_info_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True
    return False

def send_verification_email(user,email):
    try:
        subject = 'Account Activation'
        message = f'Hi {user.username}, You are Registered Successfully'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
    except Exception as e:
        return False
    return True


def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if contains_personal_info(username, password):
                error_message = "Passwords should not include personal information."
                messages.error(
                    request, error_message)
                return redirect('userRegister')
            # else:

            try:
                validate_password(
                    password=password,
                    user=User,
                    password_validators=[
                        CommonPasswordValidator(),  # Prevent common passwords
                        NumericPasswordValidator(),  # Require at least one digit
                    ],
                )
                if len(password) < 8 or len(password) > 15:
                    raise ValidationError(
                        'Password must be 8-12 characters long.')
                if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', password):
                    raise ValidationError(
                        'Password must include uppercase and lowercase letters, numbers, and special characters.')
            except ValidationError as e:
                messages.error(request, ', '.join(e.messages))
                return redirect('userRegister')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('userRegister')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('userRegister')

                user = User.objects.create_user(
                    first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                auth.login(request, user)
                user.save()
                send_verification_email(user, user.email)
                messages.success(
                    request, 'You are registered successfully')
                log_activity(user, f'Registered into the system')
                return redirect('userRegister')
        else:
            messages.error(request, 'Password do not match')
            return redirect('userRegister')
    else:
        return render(request, 'accounts/userRegister.html')


@login_required(login_url='userLogin')
def userDashboard(request):
    users=request.user
    log_activity(users, f'Access Dashboard')
    return render(request, 'accounts/userDashboard.html')


def logout(request):
    if request.method == 'POST':
        username = request.user
        auth.logout(request)
        messages.success(request, 'You are successfully logged out.')
        log_activity(username, f'User Logged Out')
        return redirect('userLogin')
    return redirect('home')


def logoutadmin(request):
    if request.method == 'POST':
        username = request.user
        if request.user.is_superuser:
            auth.logout(request)
            messages.success(request, 'You are successfully logged out.')
            log_activity(username, f'Admin Logged Out')
            return redirect('adminlogin')
    return redirect('home')


def resetPass(request):
    return render(request, 'accounts/password_reset_form.html')


@login_required
def afterlogin_view(request):
    if request.user.is_superuser:
        return redirect('adminDashboard')
    else:
        messages.error(request, "Invalid login credentials")
        return redirect('adminlogin')


@login_required(login_url='afterlogin')
def adminDashboard(request):
    if request.user.is_superuser:
        User = get_user_model()
        usercount = User.objects.all().filter(is_superuser=False).count()
        productcount = models.Product.objects.all().count()
        ordercount = Orders.objects.all().count()
        # For Pagination
        order = Orders.objects.all()
        paginator = Paginator(order, 10)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        mydict = {
            'usercount': usercount,
            'productcount': productcount,
            'ordercount': ordercount,
            'order': paged_product,
        }
        return render(request, 'accounts/adminDashboard.html', mydict)
    else:
        messages.error(request, "Invalid login credentials")
        return redirect('adminlogin')


# admin view the total product in the dashbaord
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products = models.Product.objects.all()
    products = models.Product.objects.order_by('-name')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'products': paged_product,
    }

    return render(request, 'admincontrol/admin_products.html', data)

# admin add product by clicking on + button


@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    products = models.Product.objects.all()
    productForm = ProductForm()
    if request.method == 'POST':
        productForm = ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request, 'admincontrol/admin_add_products.html', {'productForm': productForm, 'products': products})


@login_required(login_url='adminlogin')
def delete_product_view(request, pk):
    products = models.Product.objects.get(id=pk)
    products.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request, pk):
    products = models.Product.objects.get(id=pk)
    productForm = ProductForm(instance=products)
    if request.method == 'POST':
        productForm = ProductForm(
            request.POST, request.FILES, instance=products)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request, 'admincontrol/admin_update_product.html', {'productForm': productForm, 'products': products})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    order = Orders.objects.all()
    paginator = Paginator(order, 5)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'order': paged_product,
    }
    return render(request, 'admincontrol/booking.html', data)


@login_required(login_url='adminlogin')
def update_order_view(request, pk):
    order = Orders.objects.get(id=pk)
    orderForm = forms.OrderForm(instance=order)
    if request.method == 'POST':
        orderForm = forms.OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request, 'admincontrol/updateorderstatus.html', {'orderForm': orderForm})


@login_required(login_url='adminlogin')
def delete_order_view(request, pk):
    order = Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')


@login_required(login_url='adminlogin')
def view_customer(request):
    User = get_user_model()
    users = User.objects.all().order_by('username').filter(is_superuser=False)
    paginator = Paginator(users, 2)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'users': paged_product,
    }
    return render(request, 'admincontrol/view_customer.html', data)


@login_required(login_url='adminlogin')
def delete_customer_view(request, pk):
    User = get_user_model()
    users = User.objects.get(id=pk)
    users.delete()
    return redirect('view-customer')


@login_required(login_url='userLogin')
def edit_profile_view(request):
    user = User.objects.get(id=request.user.id)
    userForm = UserForm(instance=user)
    mydict = {
        'userForm': userForm,
        'user': user
    }
    if request.method == 'POST':
        userForm = UserForm(request.POST, request.FILES, instance=user)
        if userForm.is_valid():
            user.set_password(user.password)
            userForm.save()
            messages.success(request, "Account Sucessfully Updated")
            return HttpResponseRedirect('userDashboard')

    return render(request, 'usercontrol/edit_profile.html', context=mydict)


@login_required(login_url='userLogin')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "Account Sucessfully Deleted")
    return redirect('userLogin')


@login_required(login_url='userLogin')
def my_order_view(request, id):
    user = User.objects.get(id=id)
    order = Orders.objects.all()
    paginator = Paginator(order, 5)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'order': paged_product,
    }

    return render(request, 'usercontrol/myorder.html', data)
