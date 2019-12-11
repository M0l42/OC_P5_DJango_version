from django.shortcuts import render
from .models import Product, Category, Store, Favorite
from .forms import ProductForm
from django.views.generic.edit import FormView
import requests


class ProductView(FormView):
    form_class = ProductForm
    template_name = "openfoodfact/product_form.html"

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['title'] = 'Load Product'
        return context

    def form_valid(self, form):
        category = form.cleaned_data['category']
        context = self.get_context_data()
        payload = {"action": "process",
                   "page_size": 50,
                   "json": 1}
        headers = {"user-agent": "python-app/0.0.1"}
        url = 'https://fr.openfoodfacts.org/categorie/' + category.slug
        r = requests.get(url, headers=headers, params=payload)

        return render(request=self.request, template_name=self.template_name, context=context)
