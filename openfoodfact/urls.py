from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ProductView

urlpatterns = [
    path('product', ProductView.as_view(), name='product'),
]
