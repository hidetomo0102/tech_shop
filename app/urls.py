from django.urls import path
from app import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<str:category>', views.category, name='category'),
    path('product/<slug>', views.ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<slug>', views.add_to_cart, name='add_to_cart'),
    path('order/', views.CartView.as_view(), name='order'),
    path('removeitem/<slug>', views.full_remove, name='removeitem'),
    path('romovesingleitem/<slug>', views.single_remove, name='removesingleitem'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('add_wishlist/<slug>', views.add_to_wishlist, name='add_wishlist'),
    path('wishlist_to_cart/<slug>', views.wishlist_to_cart, name='wishlist_to_cart'),
    path('wishlist/delete<slug>', views.delete_from_wishlist, name='delete_from_wishlist'),
    path('add_comment/<slug>', views.add_comment, name='add_comment'),
]