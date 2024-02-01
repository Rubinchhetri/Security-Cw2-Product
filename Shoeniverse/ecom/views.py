from django.shortcuts import render
from accounts import models
from django.core.mail import send_mail
from django.contrib import messages

from accounts.activity_logger import log_activity

# Create your views here.

def home(request):
    # For showing featured Products
    featured_product = models.Product.objects.filter(is_featured=True)
    products=models.Product.objects.all()
    data = {
        'products':products,
        'featured_product': featured_product,
    }
    users=request.user
    log_activity(users, f'Access HomePage')
    return render(request, 'pages/home.html', data)

def about(request):
    users=request.user
    log_activity(users, f'Access About Page')
    return render(request, 'pages/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message =request.POST['message']
        find = request.POST['find-us']
        send_mail(
            find, #subject
            message, #message
            email, #from email
            ['rubinchhetri5@gmail.com' ], #To email
        )
        messages.success(request, "Thanks for sending the message! We'll get back to you later")
        return render(request, 'pages/home.html')
