from rest_framework import generics

from .models import EmailVerificationToken, PasswordResetToken
from .permissions import IsSelfOrAdmin
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, MyTokenObtainPairSerializer, \
    ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins

from .services import send_password_reset_email
from .tasks import send_password_reset_email_task

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


class ForgotPasswordView(APIView):
    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer
    )

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email).first()

        if user:
            token = PasswordResetToken.objects.create(
                user=user
            )

            # send_password_reset_email(user, token)

            send_password_reset_email_task.delay(
                token.id
            )

        return Response(
            {
                "detail": "If an account with this email exists, "
                          "a password reset link has been sent."
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):

    def post(self, request, token):
        reset_token = get_object_or_404(
            PasswordResetToken,
            token=token
        )

        if reset_token.is_expired():
            reset_token.delete()

            return Response(
                {"detail": "Password reset link has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = reset_token.user

        user.set_password(
            serializer.validated_data["password"]
        )
        user.save()

        reset_token.delete()

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )
