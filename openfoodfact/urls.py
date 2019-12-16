from django.urls import path
from .views import ProductView, CategoryView, ProductByCategoryView, FavoriteView, FavoriteByCategoryView, FindSubstituteView

urlpatterns = [
    path('product', ProductView.as_view(), name='product'),
    path('product/<slug>/', ProductByCategoryView.as_view(), name='sort_product'),
    path('substitute/<slug>/', FindSubstituteView.as_view(), name='find_substitute'),
    path('category', CategoryView.as_view(), name='category'),
    path('favorite', FavoriteView.as_view(), name='favorite'),
    path('category/<slug>/', FavoriteByCategoryView.as_view(), name='sort_favorite'),
]
