from rest_framework import viewsets
from app_join.models import Task, Contact, SubTask
from app_join.api.serializers import TaskSerializer, \
    ContactSerializer, SubTaskSerializer
from rest_framework.permissions import IsAuthenticated


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SubTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
