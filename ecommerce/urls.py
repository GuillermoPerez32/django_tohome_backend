from rest_framework import routers
from django.urls import path, include

from ecommerce.views import CartProductViewSet, CartViewSet, CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'carts', CartViewSet, basename='cart')
# router.register(r'cart_products', CartProductViewSet, basename='cart_product')

urlpatterns = [
    path('',include(router.urls)),
]