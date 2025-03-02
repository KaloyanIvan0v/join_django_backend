from django.urls import path, include
from rest_framework import routers
from app_user_auth.api.views import UserViewSet, RegistrationView, CustomLoginView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
