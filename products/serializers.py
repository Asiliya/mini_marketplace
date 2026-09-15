from rest_framework import serializers
from .models import Product, Category


class ProductReadSerializer(serializers.ModelSerializer):
    # final_price = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    final_price = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"

    # def get_final_price(self, obj):
    #     return obj.discount_price or obj.price


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "discount_price",
            "sku",
            "stock",
            "is_active",
            "is_featured",
            "weight",
            "category",
        ]


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = "__all__"