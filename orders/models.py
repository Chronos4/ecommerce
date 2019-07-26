from decimal import Decimal
from django.core.validators import MinValueValidator, \
    MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from coupons.models import Coupon
from shop.models import Product


class Order(models.Model):
    coupon = models.ForeignKey(Coupon,
                               on_delete=models.CASCADE,
                               related_name="orders",
                               null=True,
                               blank=True)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    first_name = models.CharField(_('first name'), max_length=200)
    last_name = models.CharField(_('last name'), max_length=200)
    email = models.EmailField(_('email'),)
    address = models.CharField(_('address'), max_length=200)
    postal_code = models.CharField(_('postal code'), max_length=200)
    city = models.CharField(_('city'), max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total - total*(self.discount/Decimal("100"))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
