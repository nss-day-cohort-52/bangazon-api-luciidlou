from django.urls import path

from .views import (FavoriteSellersList, OrderListCompleted,
                    OrderListIncomplete, ProductListMax1000,
                    ProductListMin1000)

urlpatterns = [
    path('products/min1000', ProductListMin1000.as_view()),
    path('products/max1000', ProductListMax1000.as_view()),
    path('orders/completed', OrderListCompleted.as_view()),
    path('orders/incomplete', OrderListIncomplete.as_view()),
    path('customers/fav-sellers', FavoriteSellersList.as_view()),
]
