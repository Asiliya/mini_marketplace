from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import EmailVerificationToken
from user.services import send_verification_email

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'age']
        read_only_fields = ['id', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )
        return value

    def create(self, validated_data):
        # user = User.objects.create_user(**validated_data)
        user = User.objects.create_user(
            **validated_data,
            is_verified=False
        )

        verification_token = EmailVerificationToken.objects.create(
            user=user
        )

        send_verification_email(
            user,
            verification_token
        )

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.instance

        if not user.check_password(value):
            raise serializers.ValidationError("Wrong password")

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({
                "new_password": "Passwords do not match"
            })

        validate_password(attrs["new_password"], self.instance)

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#
#     def validate(self, attrs):
#         try:
#             return super().validate(attrs)
#         except AuthenticationFailed:
#             raise AuthenticationFailed(
#                 "Incorrect login or password"
#             )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")

        user = User.objects.filter(username=username).first()

        if user and not user.is_verified:
            verification_token = (
                user.verification_tokens
                .order_by("-created_at")
                .first()
            )

            if verification_token and verification_token.is_expired():
                user.delete()

                raise AuthenticationFailed(
                    "Verification period has expired. "
                    "Please register again."
                )

            raise AuthenticationFailed(
                "Please verify your email before logging in."
            )

        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed(
                "Incorrect login or password"
            )