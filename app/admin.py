from django.contrib import admin

from .models import Item, OrderItem, Order, Payment, WishList, Category, Comment, Cart, CartItem


admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(WishList)
admin.site.register(Category)
admin.site.register(Comment)