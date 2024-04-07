from django.db import models

from accounts.models import CustomUser
from products.models import Product


class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')


class Order(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'cash', 'naqd'
        CLICK = 'click', 'click'
        PAYME = 'payme', 'payme'
        APELSIN = 'apelsin', 'apelsin'

    class OrderStatus(models.TextChoices):
        CREATED = 'created', 'created'
        PENDING = 'pending', 'pending'
        DELIVERY = 'deliver', 'deliver'
        DELIVERED = 'delivered', 'delivered'
        FINISHED = 'finished', 'finished'

    home = models.CharField(max_length=240)
    floor = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10)
    entrance = models.CharField(max_length=10)
    description = models.TextField()
    delivered_time = models.DateTimeField()
    is_call = models.BooleanField(default=True)
    subtotal_price = models.FloatField()
    delivery_price = models.FloatField()
    total_price = models.FloatField()
    payment_type = models.CharField(max_length=10,  choices=PaymentType.choices, default=PaymentType.CASH)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.CREATED)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, on_delete=models.CASCADE)


