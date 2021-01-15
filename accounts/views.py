from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from accounts.decotator import supplier_required
from accounts.models import User, Supplier
from accounts.forms import ProfileForm, UserSignupForm, LoginForm, SupplierSignUpForm
from allauth.account import views


# プロフィール画面
@method_decorator(login_required, name='dispatch')
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })


# プロフィールの編集画面
@method_decorator(login_required, name='dispatch')
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'address': user_data.address,
                'tel': user_data.tel,
            }
        )
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = User.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.address = form.cleaned_data['address']
            user_data.tel = form.cleaned_data['tel']
            user_data.save()
            return redirect('profile')
        return render(request, 'accounts/profile.html', {
            'form': form,
        })


# ログアウト画面
@method_decorator(login_required, name='dispatch')
class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


# カスタマーの登録画面
class CustomerSignupView(CreateView):
    model = User
    template_name = 'accounts/customer_signup.html'
    form_class = UserSignupForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request)
        user.is_customer = True
        login(self.request, user)
        return redirect('index')


#　サプライヤーの登録画面
class SupplierSignUpView(CreateView):
    model = User
    template_name = 'accounts/supplier_signup.html'
    form_class = SupplierSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'supplier'
        return super(SupplierSignUpView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_supplier = True
        login(self.request, user)
        return redirect('supplier:top')


# カスタマーのログイン
def customer_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form = LoginForm()
                return render(request, 'accounts/customer_login.html', {'form': form})
        else:
            form = LoginForm()
            return render(request, 'accounts/customer_login.html', {'form': form})
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'accounts/customer_login.html', context)


# サプライヤーのログイン
def supplier_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('supplier:top')
            else:
                form = LoginForm()
                return render(request, 'accounts/supplier_login.html', {'form': form})
        else:
            form = LoginForm()
            return render(request, 'accounts/supplier_login.html', {'form': form})
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'accounts/supplier_login.html', context)


# サプライヤーのログアウト画面
@method_decorator(supplier_required, name='dispatch')
class SupplierLogoutView(views.LogoutView):
    template_name = 'supplier/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')
