from django.urls import path
from accounts import views


urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('login/customer/', views.customer_login, name='customer_login'),
    path('login/supplier/', views.supplier_login, name='supplier_login'),
    path('logout/customer/', views.LogoutView.as_view(), name='customer_logout'),
    path('logout/supplier/', views.SupplierLogoutView.as_view(), name='supplier_logout'),
    path('signup/customer', views.CustomerSignupView.as_view(), name='customer_signup'),
    path('signup/supplier', views.SupplierSignUpView.as_view(), name='supplier_signup'),
]