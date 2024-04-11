from django.db.models import Sum
from rest_framework import serializers

from accounts.models import UserLocation
from accounts.serializers import UserLocationSerializer
from products.serializers import ProductSerializer
from .models import CartItem, Order


class CartItemCreateSerializer(serializers.ModelSerializer):
		class Meta:
			model = CartItem
			fields = ('quantity', 'product')


class CartItemUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = CartItem
		fields = ('quantity', 'product')


class CartItemListSerializer(serializers.ModelSerializer):
	product = ProductSerializer()

	class Meta:
		model = CartItem
		fields = ('quantity', 'total_price', 'product')


class OrderCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		exclude = ('subtotal_price', 'delivery_price', 'total_price', 'status', 'user')

	def create(self, validated_data):
		items = validated_data.pop('items', None)
		order = Order.objects.create(**validated_data)
		for item in items:
			item.user=None
			item.save()
			order.items.add(item.id)
		order.subtotal_price = order.items.aggregate(total_price=Sum('total_price'))['total_price']
		order.delivery_price = UserLocation.objects.get(user=self.context['request'].user, is_active=True).price
		order.save()
		order.get_total_price()
		return order


class OrderListSerializer(serializers.ModelSerializer):
	items = CartItemListSerializer(many=True)
	address = UserLocationSerializer()

	class Meta:
		model = Order
		exclude = ('is_call', 'payment_type', 'user', 'delivered_time')

