from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from accounts.models import Supplier


class Category(models.Model):
    name = models.CharField('カテゴリー名', max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category_tag = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='販売者')

    def __str__(self):
        return self.title


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wished_item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.wished_item.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return self.user.email


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_cart_total(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f'{self.item.title}:{self.quantity}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-ordered_date']

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_checked = models.BooleanField(default=False)

    def get_total_order(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f'{self.item.title}:{self.quantity}'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contents = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contents