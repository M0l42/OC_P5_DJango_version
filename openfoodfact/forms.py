from django import forms
from .models import Category


class ProductForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all()
    )


class CategoryForm(forms.Form):
    get_data = forms.BooleanField(initial=True)


class SubstituteForm(forms.Form):
    category = Category.objects.exclude()
