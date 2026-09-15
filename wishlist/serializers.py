from rest_framework import serializers

from carts.serializers import ProductShortSerializer
from products.models import Product
from wishlist.models import WishListItem


class WishListItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )

    class Meta:
        model = WishListItem
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        product = attrs["product"]

        if WishListItem.objects.filter(
                user=user,
                product=product
        ).exists():
            raise serializers.ValidationError(
                "Product already in wishlist."
            )

        return attrs