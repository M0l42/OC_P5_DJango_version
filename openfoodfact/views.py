from django.shortcuts import render
from .models import Product, Category, Favorite
from .forms import ProductForm, CategoryForm
from django.views.generic import ListView
from django.views.generic.edit import FormView
import requests
import json
import os


headers = {"user-agent": "python-app/0.0.1"}


def check_error(check_data, first_arg, second_arg):
    try:
        if second_arg:
            return check_data[first_arg][second_arg]
        else:
            return check_data[first_arg]
    except KeyError:
        return None


class CategoryView(FormView):
    form_class = CategoryForm
    template_name = "openfoodfact/form.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['title'] = 'Load Product'
        return context

    def form_valid(self, form):
        Category.objects.all().delete()
        get_data = form.cleaned_data['get_data']
        context = self.get_context_data()
        if get_data:
            current_path = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_path, "categories.json")
            with open(json_path, 'r') as file:
                data = json.load(file)

            categories_url = "https://fr.openfoodfacts.org/categorie/"
            for category in data['tags']:
                name = category['name']
                tag = category['id']
                url = categories_url + tag
                r = requests.get(url + ".json", headers=headers)
                product = r.json()["count"]
                Category.objects.create(name=name, tags=tag, url=url, numbers_of_product=product)

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

        for i in range(int(main_category.numbers_of_product/payload['page_size'])):
            payload['page'] = i
            data = requests.get(url, headers=headers, params=payload).json()
            for product in data["products"]:
                ingredients = check_error(product, 'ingredients_text_fr', '')
                name = check_error(product, 'product_name', '')
                if name is None:
                    name = "N/A"
                url = product['url']
                image_url = check_error(product, 'image_small_url', '')
                stores = check_error(product, 'stores', '')
                code = product['code']
                nutrition_grade = check_error(product, 'nutrition_grades', '')
                salt_100 = check_error(product, 'nutriments', 'salt_100g')
                salt_lvl = check_error(product, 'nutrient_levels', 'salt')

                sugars_100 = check_error(product, 'nutriments', 'sugars_100g')
                sugars_lvl = check_error(product, 'nutrient_levels', 'sugars')

                fat_100 = check_error(product, 'nutriments', 'fat_100g')
                fat_lvl = check_error(product, 'nutrient_levels', 'fat')

                saturated_fat_100 = check_error(product, 'nutriments', 'saturated-fat_100g')
                saturated_fat_lvl = check_error(product, 'nutrient_levels', 'saturated-fat')

                Product.objects.create(name=name, ingredients=ingredients, url=url, store=stores, code=code,
                                       nutrition_grade=nutrition_grade, category=main_category, salt_100=salt_100,
                                       salt_lvl=salt_lvl, sugar_100=sugars_100, sugar_lvl=sugars_lvl, fat_100=fat_100,
                                       fat_lvl=fat_lvl, saturated_fat_100=saturated_fat_100,
                                       saturated_fat_lvl=saturated_fat_lvl, img_url=image_url)

        return render(request=self.request, template_name=self.template_name, context=context)


class ProductByCategoryView(ListView):
    model = Product
    template_name = 'openfoodfact/catalog.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product'
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        category = Category.objects.filter(tags=self.kwargs['slug'])
        return Product.objects.filter(category=category[0])


class FindSubstituteView(ListView):
    model = Product
    template_name = 'openfoodfact/catalog.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Substitute'
        return context

    def get_queryset(self):
        category = Category.objects.filter(tags=self.kwargs['slug'])
        substitute = Product.objects.filter(category=category[0]).order_by('nutrition_grade')
        return substitute


class FavoriteView(ListView):
    model = Favorite
    template_name = 'openfoodfact/favorite.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favoris'
        context['categories'] = Category.objects.all()
        return context


class FavoriteByCategoryView(FavoriteView):
    def get_queryset(self):
        category = Category.objects.filter(tags=self.kwargs['slug'])
        return Favorite.objects.filter(category=category[0])

