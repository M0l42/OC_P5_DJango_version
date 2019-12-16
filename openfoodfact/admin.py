from django.contrib import admin
from .models import Category, Product, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tags', 'numbers_of_product')
    search_fields = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'nutrition_grade', 'category')
    search_fields = ('name', )
    list_filter = ['category']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('product', 'substitute')
    search_fields = ('product', )
    list_filter = ['product']
