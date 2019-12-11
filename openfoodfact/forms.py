from django import forms
from .models import Category


class ProductForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all()
    )
