from django.urls import path
from .views import UserViewSet, RegisterView, ChangePasswordView, MyTokenObtainPairView, VerifyEmailView, \
    ForgotPasswordView, ResetPasswordView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = [
    *router.urls,
    path('register/', RegisterView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path("token/", MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("verify-email/<uuid:token>/", VerifyEmailView.as_view(),),
    path("forgot-password/", ForgotPasswordView.as_view(),),
    path("reset-password/<uuid:token>/", ResetPasswordView.as_view(),),
]