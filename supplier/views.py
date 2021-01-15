from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from app.models import Item, OrderItem, Order, Payment, WishList, Category, Comment
from accounts.models import User, Supplier
from accounts.decotator import supplier_required
from .forms import ItemListForm


# Supplier のトップ画面
@method_decorator(supplier_required, name='dispatch')
class SupplierIndexView(View):
    def get(self, request, num=1, *args, **kwargs):

        supplier = Supplier.objects.get(user=self.request.user)

        item_data = Item.objects.filter(supplier=supplier)
        paginator = Paginator(item_data, 8)
        page = self.request.GET.get('page', 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        return render(request, 'supplier/top.html', {
            'pages': pages,
            'page_range': paginator.page_range,
            'page_active': num,
            'page_last': paginator.num_pages,
        })


# Supplier は自分の出品アイテムを確認
@method_decorator(supplier_required, name='dispatch')
class SupplierItemDetailView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])
        comments = Comment.objects.filter(item__slug=self.kwargs['slug']).order_by('-created_date')
        return render(request, 'supplier/item_detail.html', {'item_data': item_data, 'comments': comments})


# 自分の出品アイテムの情報をアップデート
@method_decorator(login_required, name='dispatch')
class SupplierItemUpdateView(UpdateView):
    model = Item
    fields = ('title', 'price', 'description', 'slug', 'category_tag', 'image')
    success_url = reverse_lazy('supplier:detail')
    template_name = 'supplier/update_item.html'

    def get_queryset(self):
        base_query = super(SupplierItemUpdateView, self).get_queryset()
        return base_query.filter(supplier=Supplier.objects.get(user=self.request.user))

    def get_success_url(self, *args, **kwargs):
        return reverse('supplier:detail', kwargs={'slug': self.kwargs['slug']})


# 自分の出品アイテムを削除
@method_decorator(supplier_required, name='dispatch')
class SupplierItemDeleteView(DeleteView):
    template_name = 'supplier/delete_confirm.html'
    model = Item
    success_url = reverse_lazy('supplier:top')

    def get_queryset(self):
        base_query = super(SupplierItemDeleteView, self).get_queryset()
        return base_query.filter(supplier=Supplier.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super(SupplierItemDeleteView, self).get_context_data(**kwargs)
        item_data = Item.objects.get(slug=self.kwargs['slug'])

        context['item_data'] = item_data
        return context


# 新規アイテムの出品
@method_decorator(supplier_required, name='dispatch')
class SupplierItemCreateView(CreateView, LoginRequiredMixin):
    model = Item
    form_class = ItemListForm
    template_name = 'supplier/list_item.html'
    success_url = reverse_lazy('supplier:top')

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.supplier = Supplier.objects.get(user=self.request.user)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self,*args, **kwargs):
        context = super(SupplierItemCreateView, self).get_context_data(*args, **kwargs)
        supplier = Supplier.objects.get(user=self.request.user)
        category = Category.objects.all()

        context['supplier'] = supplier
        context['category'] = category
        return context


# 注文が入ったら通知する
@supplier_required
def order_notification(request):
    supplier = Supplier.objects.get(user=request.user)

    order_items = OrderItem.objects.filter(item__supplier=supplier)

    return render(request, 'supplier/notification.html', {'order_items': order_items.order_by('-order__ordered_date')})


# 注文を確認する
@supplier_required
def order_check(request, id):

    order_item = get_object_or_404(OrderItem, id=id)
    order_item.is_checked = True
    order_item.save()
    return redirect('supplier:order')
