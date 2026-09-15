from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .permissions import IsAuthorOrAdmin
from .serializers import ProductReadSerializer, ProductWriteSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets
from django.core.cache import cache
from rest_framework.response import Response

class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.all()
    queryset = Product.objects.select_related("category")
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductWriteSerializer
        return ProductReadSerializer

    def perform_create(self, serializer):
        product = serializer.save(author=self.request.user)

        cache.delete("products:list")

        if product.category:
            cache.delete(
                f"products:category:{product.category.slug}"
            )

    def get_queryset(self):
        queryset = super().get_queryset()

        # category_id = self.request.query_params.get("category")
        #
        # if category_id:
        #     queryset = queryset.filter(category_id=category_id)

        category_slug = self.request.query_params.get("category")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def list(self, request, *args, **kwargs):
        category_slug = request.query_params.get("category")

        if category_slug:
            cache_key = f"products:category:{category_slug}"
        else:
            cache_key = "products:list"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        data = serializer.data

        cache.set(
            cache_key,
            data,
            timeout=60 * 5
        )

        return Response(data)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
