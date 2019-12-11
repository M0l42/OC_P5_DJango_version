from django.contrib import admin
from .models import Store, Category, Product, Favorite


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'nutrition_grade', 'category')
    search_fields = ('name', )
    list_filter = ['category']
    filter_vertical = ['sub_category', 'store']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('product', 'substitute')
    search_fields = ('product', )
    list_filter = ['product']
