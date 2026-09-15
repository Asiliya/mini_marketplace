from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wishlist.views import WishListItemViewSet

router = DefaultRouter()
router.register(r'wishlist', WishListItemViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]