from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from carts.permissions import IsCartOwner
from wishlist.models import WishListItem
from wishlist.serializers import WishListItemSerializer

from rest_framework import mixins, viewsets


class WishListItemViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = WishListItemSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

    def get_queryset(self):
        return WishListItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
