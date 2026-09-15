from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer
from .permissions import IsCartOwner
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]


    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        user = self.request.user

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": serializer.validated_data.get("quantity", 1)}
        )

        if not created:
            new_quantity = (
                    cart_item.quantity +
                    serializer.validated_data.get("quantity", 1)
            )

            if new_quantity > product.stock:
                raise serializers.ValidationError({
                    "quantity": "Not enough items in stock."
                })

            cart_item.quantity = new_quantity
            cart_item.save()

            # cart_item.quantity += serializer.validated_data.get("quantity", 1)
            # cart_item.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        cart_total = sum(
            item.total_price for item in queryset
        )

        return Response({
            "items": serializer.data,
            "cart_total": cart_total
        })
