from rest_framework import serializers

from products.models import Product
from .models import CartItem


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "final_price",
            "price",
            "discount_price",
            "sku",
            "stock",
            "is_active",
            "is_featured",
            "weight",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["user"]

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get("request")

        if request and request.method in ["PUT", "PATCH"]:
            fields.pop("product_id", None)

        return fields

    def validate(self, attrs):
        product = attrs.get("product")
        if not product and self.instance:
            product = self.instance.product

        quantity = attrs.get(
            "quantity",
            self.instance.quantity if self.instance else 1
        )

        if quantity > product.stock:
            raise serializers.ValidationError({
                "quantity": "Not enough items in stock."
            })

        return attrs