from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .permissions import IsAuthorOrAdmin
from .serializers import ProductReadSerializer, ProductWriteSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets

class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.all()
    queryset = Product.objects.select_related("category")
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductWriteSerializer
        return ProductReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
