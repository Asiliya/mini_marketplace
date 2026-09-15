from django.urls import path
from .views import UserViewSet, RegisterView, ChangePasswordView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = [
    *router.urls,
    path('register/', RegisterView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]