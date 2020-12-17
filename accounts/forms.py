from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Supplier


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=50, label='ユーザー名', required=False)
    first_name = forms.CharField(max_length=30, label='名')
    last_name = forms.CharField(max_length=30, label='性')
    address = forms.CharField(max_length=30, label='住所', required=False)
    tel = forms.CharField(max_length=30, label='電話番号')


class UserSignupForm(UserCreationForm):
    last_name = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    tel = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, required=True)
    address = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['last_name', 'first_name', 'email', 'tel']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.email = self.cleaned_data['email']
            user.tel = self.cleaned_data['tel']
            user.last_name = self.cleaned_data['last_name']
            user.first_name = self.cleaned_data['first_name']
            user.address = self.cleaned_data['address']
            user.save()
        return user


class SupplierSignUpForm(UserCreationForm):
    last_name = forms.CharField(max_length=50, label='性')
    first_name = forms.CharField(max_length=50, label='名')
    address = forms.CharField(max_length=100, label='住所')
    company_name = forms.CharField(max_length=100, required=True, label='会社名（販売者名）')
    email = forms.EmailField(max_length=100, required=True)
    tel = forms.CharField(max_length=50, label='電話番号')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'company_name', 'last_name', 'first_name', 'tel', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_supplier = True
        if commit:
            user.email = self.cleaned_data['email']
            user.last_name = self.cleaned_data['last_name']
            user.first_name = self.cleaned_data['first_name']
            user.tel = self.cleaned_data['tel']
            user.address = self.cleaned_data['address']
            user.save()
            company_name = self.cleaned_data['company_name']
            supplier = Supplier.objects.create(user=user, company_name=company_name)
            supplier.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)