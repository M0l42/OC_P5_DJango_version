from django.urls import path
from .views import ProductView, CategoryView

urlpatterns = [
    path('product', ProductView.as_view(), name='product'),
    path('category', CategoryView.as_view(), name='category'),
]
