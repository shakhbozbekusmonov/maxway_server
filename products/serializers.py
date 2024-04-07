from rest_framework import serializers
from common.serializers import MediaSerializer
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductImageSerializer(serializers.ModelSerializer):
    image = MediaSerializer()

    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'desc', 'price', 'category', 'images')

    def get_images(self, obj):
        product_images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(product_images, many=True).data


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'products')


