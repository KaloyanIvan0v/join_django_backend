from django.urls import path, include
from rest_framework import routers
from app_join.api.views import TaskViewSet, ContactViewSet, SubTaskViewSet


router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'subtasks', SubTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
