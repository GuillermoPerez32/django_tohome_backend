from asyncore import read
from email.policy import default
from itertools import product
from rest_framework import serializers
from directorio.models import User
from ecommerce.models import Cart, Cart_Product, Category, Product, Rating


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = ('__all__')


class ProductSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())

    class Meta:

        model = Product

        fields = (
            'uuid',
            'name',
            'categories',
            'price',
            'image',
            'stock',
            'description',
            'rating',
            'week_sell',
        )
        read_only_fields = ('uuid',)


class RatingSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True))
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    rate = serializers.IntegerField(max_value=5, min_value=1)

    class Meta:

        model = Rating

        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['user']
        rate = validated_data['rate']
        product = validated_data['product']
        return Rating.objects.update_or_create(user=user, product=product, defaults={'rate': rate})


class CartProductSerializer(serializers.ModelSerializer):

    id_product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    name = serializers.CharField(
        required=False,
        read_only=True
    )
    total_price = serializers.IntegerField(
        required=False,
        read_only=True
    )

    class Meta:

        model = Cart_Product
        exclude = ('id_cart', 'id')
        read_only_fields = ('total_price', 'name')


class CartSerializer(serializers.ModelSerializer):

    id_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = CartProductSerializer(
        many=True
    )
    cart_price = serializers.IntegerField(
        required=False,
        read_only=True
    )

    def validate(self, attrs):

        print(attrs)
        print(type(attrs))
        print(attrs['products'])
        list = attrs['products']

        print(list)
        print(type(list))

        for item in list:
            # Here you write the validations of the product list
            if item['stock'] > item['id_product'].stock:
                raise serializers.ValidationError('There is no available quantity for the product {}. Currently there are {} in the store'.format(
                    item['id_product'].name, item['id_product'].stock))

        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        products = validated_data['products']
        cart = Cart.objects.create(id_user=validated_data['id_user'])

        for product in products:
            object = Cart_Product.objects.create(
                id_cart=cart, **product).save()
            product['id_product'].stock -= product['stock']
            product['id_product'].save()

        return cart

    class Meta:

        model = Cart
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'cart_price')
