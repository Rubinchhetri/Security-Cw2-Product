from django.db import models


# Create your models here.

class Product(models.Model):
    available_choice = (
        ('In Stock', 'In Stock'),
        ('Out Of Stock', 'Out Of Stock'),
    )
    name = models.CharField(max_length=40)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)      
    category=models.CharField(max_length=40)
    price = models.PositiveIntegerField()
    available = models.CharField(choices=available_choice, max_length=40)
    description=models.CharField(max_length=40)
    is_featured = models.BooleanField(default=False)
    def __str__(self):
        return self.name