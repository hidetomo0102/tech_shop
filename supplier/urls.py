from django.urls import path

from .views import SupplierIndexView, SupplierItemDetailView, SupplierItemUpdateView, SupplierItemDeleteView, SupplierItemCreateView, order_notification, order_check

app_name = 'supplier'

urlpatterns = [
    path('', SupplierIndexView.as_view(), name='top'),
    path('order/', order_notification, name='order'),
    path('order_check/<int:id>', order_check, name='order_check'),
    path('create/', SupplierItemCreateView.as_view(), name='create'),
    path('detail/<slug>', SupplierItemDetailView.as_view(), name='detail'),
    path('update/<slug>', SupplierItemUpdateView.as_view(), name='update'),
    path('delete/<slug>', SupplierItemDeleteView.as_view(), name='delete'),
]