from django.urls import path
from .views import ProductListMin1000, ProductListMax1000

urlpatterns = [
    path('products/min1000', ProductListMin1000.as_view()),
    path('products/max1000', ProductListMax1000.as_view()),
]
