from ast import Raise
from django.contrib import admin
from django_restful_admin import admin as rest_admin

from ecommerce.models import Cart, Cart_Product, Category, Product, Rating


#Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Cart_Product)
admin.site.register(Rating)

rest_admin.site.register(Product)
rest_admin.site.register(Category)
rest_admin.site.register(Cart)
rest_admin.site.register(Cart_Product)
rest_admin.site.register(Rating)