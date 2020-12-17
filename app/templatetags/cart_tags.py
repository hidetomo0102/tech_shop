from django import template

from app.models import CartItem

register = template.Library()


@register.filter(name='itemCount')
def itemCount(user):
    if user.is_authenticated:
        cart_item = CartItem.objects.filter(cart__user=user)
        if cart_item.exists():
            return cart_item.count()
        else:
            return 0