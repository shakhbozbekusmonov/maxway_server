from rest_framework import serializers
from common.serializers import MediaSerializer
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = MediaSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'desc', 'price', 'category', 'image')


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'products')


