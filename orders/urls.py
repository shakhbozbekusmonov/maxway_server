from django.urls import path
from .views import CartItemCreateAPIView, CartItemUpdateAPIView, CartItemListAPIView, TotalPriceInfoAPIView, \
	OrderCreateAPIView, OrderListAPIView

urlpatterns = [
	path('cart-item-create/', CartItemCreateAPIView.as_view(), name='cart-item-create'),
	path('cart-item-update/', CartItemUpdateAPIView.as_view(), name='cart-item-update'),
	path('cart-item-list/', CartItemListAPIView.as_view(), name='cart-item-list'),
	path('total-price-info/', TotalPriceInfoAPIView.as_view(), name='total-price-info'),
	path('order-create/', OrderCreateAPIView.as_view(), name='order-create'),
	path('order-list/', OrderListAPIView.as_view(), name='order-list'),
]
