from django.urls import path
from .views import ProductFormView, CategoryView, ProductByCategoryView, FavoriteView, \
    FavoriteByCategoryView, FindSubstituteView, SaveSubstituteView, ProductView, HomeView

urlpatterns = [
    path('load-product', ProductFormView.as_view(), name='load_product'),
    path('load-category', CategoryView.as_view(), name='load_category'),
    path('', HomeView.as_view(), name='home'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<category>/', ProductByCategoryView.as_view(), name='sort_product'),
    path('product/<category>/<int:product>/', FindSubstituteView.as_view(), name='find_substitute'),
    path('product/<category>/<int:product>/<int:substitute>', SaveSubstituteView.as_view(), name='save_favorite'),
    path('favorite', FavoriteView.as_view(), name='favorite'),
    path('favorite/<slug>/', FavoriteByCategoryView.as_view(), name='sort_favorite'),
]
