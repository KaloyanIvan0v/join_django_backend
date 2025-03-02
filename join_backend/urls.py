from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app_join.api.urls')),
    path('api/v1/auth/', include('app_user_auth.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
