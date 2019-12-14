from django.shortcuts import render
from .models import Product, Category, Store, Favorite
from .forms import ProductForm, CategoryForm
from django.views.generic import ListView
from django.views.generic.edit import FormView
import requests
import json
import os


# payload = {"action": "process",
#            "page_size": 50,
#            "json": 1}
headers = {"user-agent": "python-app/0.0.1"}


class CategoryView(FormView):
    form_class = CategoryForm
    template_name = "openfoodfact/form.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['title'] = 'Load Product'
        return context

    def form_valid(self, form):
        get_data = form.cleaned_data['get_data']
        context = self.get_context_data()
        if get_data:
            r = requests.get('https://fr.openfoodfacts.org/categories', headers=headers, params=payload)
            data = r.json()
            for category in data['tags']:
                name = category['name']
                tag = category['id']
                url = category['url']
                numbers_of_product = category['products']
                Category.objects.create(name=name, tags=tag, url=url, numbers_of_product=numbers_of_product)

        return render(request=self.request, template_name=self.template_name, context=context)


class ProductView(FormView):
    form_class = ProductForm
    template_name = "openfoodfact/form.html"

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['title'] = 'Load Product'
        return context

    def form_valid(self, form):
        main_category = form.cleaned_data['category']
        payload = {"action": "process",
                   "tagtype_0": "categories",
                   "tag_contains_0": "contains",
                   "tag_0": main_category.tags,
                   "page_size": 50,
                   "sort_by": "unique_scans_n",
                   "json": 1}
        context = self.get_context_data()
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        r = requests.get(url, headers=headers, params=payload)
        data = r.json()

        # with open(json_path, 'w') as file:
        #     data = r.json()
        #     json.dump(data, file, indent=2)

        for product in data["products"]:
            try:
                ingredients = product['ingredients_text_fr']
            except KeyError:
                ingredients = product['ingredients_text']
            try:
                name = product['product_name_fr']
            except KeyError:
                name = product['product_name']
            stores = product['stores'].split(", ")
            categories = product['categories_tags']
            code = product['code']
            try:
                nutrition_grade = product['nutrition_grades']
            except KeyError:
                nutrition_grade = ''

            new_product = Product.objects.create(name=name, ingredients=ingredients,
                                                 nutrition_grade=nutrition_grade, category=main_category, code=code)

            for store in stores:
                try:
                    product_store = Store.objects.get(name=store)
                except Store.DoesNotExist:
                    if store:
                        product_store = Store.objects.create(name=store, slug=store)
                    else:
                        product_store = None

                if product_store:
                    new_product.store.add(product_store)
                    new_product.save()

            for category in categories:
                product_category = Category.objects.get(tags=category)
                new_product.sub_category.add(product_category)
                new_product.save()

        return render(request=self.request, template_name=self.template_name, context=context)


class ProductByCategoryView(ListView):
    model = Product
    template_name = 'openfoodfact/catalog.html'
    paginate_by = 20
    ordering = ['nutrition_grade']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product'
        return context

    def get_queryset(self):
        category = Category.objects.filter(tags=self.kwargs['slug'])
        return Product.objects.filter(category=category[0])
