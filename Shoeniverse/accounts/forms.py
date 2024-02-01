from django import forms
from . import models

from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        available_choice = (
            ('In Stock', 'In Stock'),
            ('Out Of Stock', 'Out Of Stock'),
        )
        available = forms.ChoiceField(required=True, choices=available_choice)
        fields = ['name', 'category', 'price', 'available', 'description', 'is_featured', 'product_image']
