from django import forms
from django.contrib.auth import forms as auth_forms

from app.models import Item
from accounts.models import Supplier


class ItemListForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'price', 'category_tag', 'slug', 'description', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '記入例: MacBook Pro 13 inch'}),
            'price': forms.NumberInput(attrs={'min': 1}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }