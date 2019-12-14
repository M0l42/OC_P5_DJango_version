from django.urls import path
from .views import ProductView, CategoryView, ProductByCategoryView

urlpatterns = [
    path('product', ProductView.as_view(), name='product'),
    path('product/<slug>/', ProductByCategoryView.as_view(), name='sort_product'),
    path('category', CategoryView.as_view(), name='category'),
]
