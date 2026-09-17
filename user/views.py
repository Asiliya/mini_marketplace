from rest_framework import generics

from .models import EmailVerificationToken
from .permissions import IsSelfOrAdmin
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, MyTokenObtainPairSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
User = get_user_model()

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class VerifyEmailView(APIView):

    def get(self, request, token):
        verification_token = get_object_or_404(
            EmailVerificationToken,
            token=token
        )

        if verification_token.is_expired():
            verification_token.user.delete()

            return Response(
                {"detail": "Verification link has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = verification_token.user

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        verification_token.delete()

        return Response(
            {"detail": "Email successfully verified."},
            status=status.HTTP_200_OK
        )
