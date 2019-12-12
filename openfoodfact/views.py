from django.shortcuts import render
from .models import Product, Category, Store, Favorite
from .forms import ProductForm, CategoryForm
from django.views.generic.edit import FormView
import requests
import json
import os


payload = {"action": "process",
           "page_size": 50,
           "json": 1}
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
        context = self.get_context_data()
        url = 'https://fr.openfoodfacts.org/categorie/' + main_category.slug
        r = requests.get(url, headers=headers, params=payload)
        data = r.json()

        # with open(json_path, 'w') as file:
        #     data = r.json()
        #     json.dump(data, file, indent=2)

        for product in data["products"]:
            nutrition_grade = product['nutrition_grades']
            ingredients = product['ingredients_text_fr']
            name = product['product_name_fr']
            stores = product['stores'].split(", ")
            categories = product['categories'].split(", ")
            if len(categories) == 1:
                categories = product['categories'].split(",")
            categories_tag = product['categories_tags']

            new_product = Product.objects.create(name=name, ingredients=ingredients,
                                                 nutrition_grade=nutrition_grade, category=main_category)

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

            for i, category in enumerate(categories):
                try:
                    product_category = Category.objects.get(slug=categories_tag[i])
                except Category.DoesNotExist:
                    product_category = Category.objects.create(name=category, slug=categories_tag[i])

                if product_category.name != main_category.name:
                    new_product.sub_category.add(product_category)
                    new_product.save()

        return render(request=self.request, template_name=self.template_name, context=context)
