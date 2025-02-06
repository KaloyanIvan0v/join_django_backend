from django.urls import path, include
from rest_framework import routers
from app_join.api.views import TaskViewSet,  SubTaskViewSet, \
    ContactViewSet,  UserViewSet


router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
