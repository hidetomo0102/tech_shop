from django import template

from app.models import OrderItem, Order

register = template.Library()


@register.filter(name='orderCount')
def orderCount(user):
    if user.is_authenticated:
        ordered_item = OrderItem.objects.filter(item__supplier__user=user, is_checked=False)
        if ordered_item.exists():
            return ordered_item.count()
        else:
            return 0