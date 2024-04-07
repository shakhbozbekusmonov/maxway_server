from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer, CategoryWithProductsSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CategoryRetrieveView(RetrieveAPIView):
    serializer_class = CategoryWithProductsSerializer

    def get_queryset(self):
        return Category.objects.prefetch_related('products').all()

