from django.db import IntegrityError
from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserLocation
from .serializers import CartItemCreateSerializer, CartItemUpdateSerializer, CartItemListSerializer, \
    OrderCreateSerializer, OrderListSerializer
from .models import CartItem, Order


class CartItemCreateAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)

            return Response(data={"message": "success"})
        except IntegrityError as e:
            return Response({
                "message": "This product has already been created and will be deleted",
                "code": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({
                "message": "Product does not exists",
                "code": 400
            })


class CartItemUpdateAPIView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        cart_item = CartItem.objects.get(user=request.user, product=data.get('product'))
        cart_item.quantity = data.get('quantity') if 'quantity' in data else cart_item.quantity
        cart_item.save()
        return Response(data={'result': cart_item.id}, status=status.HTTP_200_OK)


class CartItemListAPIView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TotalPriceInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products_total_price = CartItem.objects.filter(user=request.user).aggregate(total_price=Sum('total_price'))['total_price']
        delivery_address = UserLocation.objects.get(user=request.user, is_active=True)
        total_price = products_total_price + delivery_address.price
        result = {
            "sub_total_price": products_total_price,
            "delivery_price": delivery_address.price,
            "total_price": total_price
        }

        return Response(data=result)


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {
            "request": self.request,
            "view": self
        }


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    pagination_class = None
