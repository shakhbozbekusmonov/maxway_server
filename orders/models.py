from django.db import models
from django.db.models import Sum

from accounts.models import CustomUser, UserLocation
from products.models import Product


class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')

    class Meta:
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        return super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.product.name)


class Order(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'cash', 'naqd'
        CLICK = 'click', 'click'
        PAYME = 'payme', 'payme'
        APELSIN = 'apelsin', 'apelsin'

    class OrderStatus(models.TextChoices):
        CREATED = 'created'
        ACCEPTED = 'accepted'
        PREPARED = 'prepared'
        DELIVERING = 'delivering'
        DELIVERED = 'delivered'

    home = models.CharField(max_length=240)
    floor = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10)
    entrance = models.CharField(max_length=10)
    description = models.TextField()
    delivered_time = models.DateTimeField()
    is_call = models.BooleanField(default=True)
    subtotal_price = models.FloatField(null=True)
    delivery_price = models.FloatField(null=True)
    total_price = models.FloatField(null=True)
    payment_type = models.CharField(max_length=10,  choices=PaymentType.choices, default=PaymentType.CASH)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.CREATED)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    address = models.ForeignKey(UserLocation, on_delete=models.SET_NULL, null=True)

    def get_total_price(self):
        self.total_price = self.items.aggregate(total_price=Sum('total_price'))['total_price'] + self.delivery_price
        self.save()
        return self.total_price
