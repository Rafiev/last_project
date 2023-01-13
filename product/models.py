from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    title = models.SlugField(primary_key=True, unique=True)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='images/')