from rest_framework import generics

from .permissions import IsSelfOrAdmin
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets, mixins
User = get_user_model()

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(
            instance=request.user,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK
        )
