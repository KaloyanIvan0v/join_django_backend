from rest_framework import serializers
from app_join.models import Task, SubTask, Contact


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'state', 'description']
        read_only_fields = ['id']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'author', 'checkbox', 'color',
                  'email', 'name', 'nameInitials', 'phone']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    subTasks = SubTaskSerializer(many=True, required=False)
    assignedTo = ContactSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'state', 'prio',
            'dueDate', 'category', 'subTasks', 'assignedTo',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):

        rep = super().to_representation(instance)
        contacts = instance.assignedTo.all()
        rep['assignedTo'] = ContactSerializer(contacts, many=True).data
        return rep

    def create(self, validated_data):

        sub_tasks_data = validated_data.pop('subTasks', [])
        assigned_to_data = validated_data.pop('assignedTo', [])

        task = Task.objects.create(**validated_data)

        contact_ids = [Contact.objects.get(
            email=contact['email']).id for contact in assigned_to_data]
        task.assignedTo.set(contact_ids)

        for sub_task_data in sub_tasks_data:
            SubTask.objects.create(parentTask=task, **sub_task_data)

        return task

    def update(self, instance, validated_data):
        sub_tasks_data = validated_data.pop('subTasks', None)
        assigned_to_data = validated_data.pop('assignedTo', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if assigned_to_data is not None:
            instance.assignedTo.clear()
            contact_ids = [Contact.objects.get(
                email=contact['email']).id for contact in assigned_to_data]
            instance.assignedTo.set(contact_ids)

        if sub_tasks_data is not None:
            instance.subTasks.all().delete()
            for sub_task_data in sub_tasks_data:
                SubTask.objects.create(parentTask=instance, **sub_task_data)

        return instance
