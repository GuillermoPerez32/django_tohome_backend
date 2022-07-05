from datetime import timedelta
from itertools import product
import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from directorio.models import User

# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})

class Product(models.Model):
    
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    name = models.CharField(
        _('product\'s name'),
        max_length=64,
        unique=True
        )
    categories = models.ManyToManyField(
        Category,
        blank=True
        )
    price = models.IntegerField(_('price'))
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField()
    description = models.TextField()
    created_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name

    @property
    def week_sell(self):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        sells = self.cart_product_set.filter(id_cart__created_at__gte = some_day_last_week)
        return sum([sell.stock for sell in sells])

    @property
    def rating(self):
        return self.rating_set.aggregate(models.Avg('rate'))['rate__avg'] or 0

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"uuid": self.uuid})

class Rating(models.Model):
    """Model definition for Rating."""

    user = models.ForeignKey(get_user_model(), models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    rate = models.PositiveSmallIntegerField()

    class Meta:
        """Meta definition for Rating."""

        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        """Unicode representation of Rating."""
        return f'{self.user.username} => {self.product.name} => {self.rate}'

class Cart(models.Model):
    
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    id_user = models.ForeignKey(User, verbose_name=_("user\'s ID"), on_delete=models.PROTECT)
    state = models.CharField(_("cart\'s state"), max_length=15, default='espera')
    created_at = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = "cart"
        verbose_name_plural = "carts"
        
    @property
    def products(self):
        return self.cart_product_set.all()
    
    @property
    def cart_price(self):
        objects = self.cart_product_set.all()
        total = sum([objet.total_price for objet in objects])
        return total

    def __str__(self):
        return str(self.uuid)

    def get_absolute_url(self):
        return reverse("cart-detail", kwargs={"uuid": self.uuid})

class Cart_Product(models.Model):
    
    id_product = models.ForeignKey(
            Product,
            on_delete=models.PROTECT,
            verbose_name=_('Product ID'),
    )
    id_cart = models.ForeignKey(
            Cart,
            on_delete=models.PROTECT,
            verbose_name=_('Cart ID')
    )
    stock = models.IntegerField()
    
    
    class Meta:
        verbose_name = "cart_product"
        verbose_name_plural = "cart_products"
        
    @property
    def total_price(self):
        return self.id_product.price * self.stock
    
    @property
    def name(self):
        return self.id_product.name
        
    def __str__(self):
        return self.id_product.name

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"uuid": self.id_product + '->' + self.id_cart})