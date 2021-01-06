from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Item, OrderItem, Order, Payment, WishList, Category, Comment, Cart, CartItem
from accounts.models import User
from .forms import CommentForm

import stripe


class IndexView(View):
    def get(self, request, num=1, *args, **kwargs):

        keyword = self.request.GET.get('keyword')

        if keyword:
            item_data = Item.objects.filter(
                Q(title__contains=keyword) | Q(description__contains=keyword)
            )
        else:
            item_data = Item.objects.all()
        paginator = Paginator(item_data, 8)
        page = self.request.GET.get('page', 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        csrf_token = self.request.GET.get('csrfmiddelewaretoken')
        category_list = Category.objects.all()
        return render(request, 'app/index.html', {
            'keyword': keyword,
            'category_list': category_list,
            'pages': pages,
            'page_range': paginator.page_range,
            'page_active': num,
            'page_last': paginator.num_pages,
            'csrf_token': csrf_token
        })


def category(request, category, num=1):
    category_list = Category.objects.all()
    category = Category.objects.get(name=category)
    item_data = Item.objects.filter(category_tag=category)
    paginator = Paginator(item_data, 8)
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'app/category.html', {
        'category_list': category_list,
        'pages': pages,
        'page_range': paginator.page_range,
        'page_active': num,
        'page_last': paginator.num_pages
    })


class ItemDetailView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])

        comments = Comment.objects.filter(item__slug=self.kwargs['slug']).order_by('-created_date')
        return render(request, 'app/product.html', {
            'item_data': item_data,
            'comments': comments,
        })


@login_required(login_url='/accounts/login/customer/')
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()

    try:
        cart_item = CartItem.objects.get(item=item, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(item=item, cart=cart)
        cart_item.save()
    return redirect('order')


@method_decorator(login_required, name='dispatch')
class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            total = 0
            for cart_item in cart_items:
                total += cart_item.get_cart_total()

            context = {'cart_items': cart_items, 'total': total}
            return render(request, 'app/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')


@login_required
def full_remove(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(item=item, cart=cart)

    cart_item.delete()
    return redirect('order')


@login_required
def single_remove(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(item=item, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('order')


@method_decorator(login_required, name='dispatch')
class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order
            }
            return render(request, 'app/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')


@method_decorator(login_required, name='dispatch')
class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        total = 0
        for cart_item in cart_items:
            total += cart_item.get_cart_total()
        user_data = User.objects.get(id=request.user.id)
        context = {
            'total': total,
            'user_data': user_data
        }
        return render(request, 'app/payment.html', context)

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        order = Order.objects.create(user=request.user)

        total = 0
        item_list = []
        for cart_item in cart_items:
            total += cart_item.get_cart_total()
            item_list.append(str(cart_item.item) + ':' + str(cart_item.quantity))
            order_item = OrderItem.objects.create(order=order, item=cart_item.item, quantity=cart_item.quantity)
            order_item.save()
        cart_items.delete()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST.get('stripeToken')
        description = ' '.join(item_list)
        amount = total

        charge = stripe.Charge.create(
            amount=amount,
            currency='jpy',
            description=description,
            source=token
        )

        payment = Payment(user=request.user)
        payment.stripe_charge_id = charge['id']
        payment.amount = amount
        payment.save()

        order.payment = payment
        order.save()
        return redirect('thanks')


@method_decorator(login_required, name='dispatch')
class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/thanks.html')


@login_required
def add_to_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)

    is_wished_count = WishList.objects.filter(wished_item__slug=slug, user=request.user).count()
    if is_wished_count > 0:
        is_wished_item = WishList.objects.get(wished_item__slug=slug, user=request.user)
        message = f'{is_wished_item.wished_item.title}は既にリストへ追加されています'
        messages.success(request, message)
        return redirect('product', slug=slug)
    wished_item, created = WishList.objects.get_or_create(wished_item=item, user=request.user)
    wished_item.save()
    message = f'{wished_item.wished_item.title}をリストへ追加しました！'
    messages.info(request, message)
    return redirect('product', slug=slug)


@login_required
def delete_from_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wished_item = WishList.objects.filter(user=request.user, wished_item__slug=item.slug)

    if wished_item.exists():
        wished_item.delete()
    return redirect('wishlist')


@method_decorator(login_required, name='dispatch')
class WishListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            wished_items = WishList.objects.filter(user=request.user)
            context = {
                'wished_items': wished_items
            }
            return render(request, 'app/wishlist.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/wishlist.html')


@login_required(login_url='/accounts/login/customer/')
def wishlist_to_cart(request, slug):
    add_to_cart(request, slug)

    item = get_object_or_404(Item, slug=slug)
    wished_item = WishList.objects.filter(user=request.user, wished_item__slug=item.slug)

    if wished_item.exists():
        wished_item.delete()
    return redirect('order')


@login_required
def add_comment(request, slug):
    item = get_object_or_404(Item, slug=slug)
    item_data = Item.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = item
            comment.user = request.user
            comment.save()
            return redirect('product', slug=item.slug)
    else:
        form = CommentForm()
    return render(request, 'app/parts/add_comment.html', {'form': form, 'item_data': item_data})
