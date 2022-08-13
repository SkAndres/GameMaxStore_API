from api.models import Product, Category
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "category_id",
            "image", "title",
            "color", "memory", "price",
            "description", "quantity"
        ]
