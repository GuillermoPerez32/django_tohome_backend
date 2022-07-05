from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db import transaction
from django.utils import timezone

from datetime import timedelta

from ecommerce.models import Cart, Cart_Product, Category, Product

from ecommerce.serializers import CartProductSerializer, CartSerializer, CategorySerializer, ProductSerializer, RatingSerializer

# Create your views here.


class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    # queryset = Product.objects.filter(stock__gt = 0)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    filterset_fields = ['categories']
    search_fields = ['name']

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated],
        serializer_class=RatingSerializer
    )
    def rate(self, request, pk=None):
        """Rate product"""
        product = self.get_object()
        user = request.user

        data = request.data
        data['user'] = user.id
        data['product'] = product.uuid
        
        serializer = RatingSerializer(data=data)

        serializer.is_valid(True)
        serializer.save()

        return Response(status = status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=False,
    )
    def more_selleds(self, request):
        selleds = [product for product in Product.objects.all() if product.week_sell > 0]
        products = sorted(selleds, key=lambda product: product.week_sell, reverse=True)[:10]
        serializer = ProductSerializer(products, many = True)
        return Response(data=serializer.data, status= status.HTTP_200_OK)
        


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []


class CartViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            Cart.objects.filter(id_user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CartProductViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Cart_Product.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]
