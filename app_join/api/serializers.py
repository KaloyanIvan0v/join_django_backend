from rest_framework import serializers
from app_join.models import Task, SubTask, Contact, User


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
    # Für die Ausgabe: verschachtelte Darstellung der SubTasks
    subTasks = SubTaskSerializer(many=True, required=False)
    # Beim Schreiben: Es werden Contact-IDs erwartet, da im Frontend mit existierenden Contacts gearbeitet wird.
    assignedTo = ContactSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'state', 'prio',
            'dueDate', 'category', 'subTasks', 'assignedTo',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        Überschreibt die Repräsentation, sodass bei der Ausgabe statt
        einer Liste von IDs detaillierte Contact-Daten angezeigt werden.
        """
        rep = super().to_representation(instance)
        contacts = instance.assignedTo.all()
        rep['assignedTo'] = ContactSerializer(contacts, many=True).data
        return rep

    def create(self, validated_data):
        # Verschachtelte SubTasks und Many-to-Many-Daten extrahieren
        sub_tasks_data = validated_data.pop('subTasks', [])
        assigned_to_data = validated_data.pop('assignedTo', [])

        # Task ohne Many-to-Many-Felder erstellen
        task = Task.objects.create(**validated_data)

        # Extract IDs from contact objects and set the relationship
        contact_ids = [Contact.objects.get(
            email=contact['email']).id for contact in assigned_to_data]
        task.assignedTo.set(contact_ids)

        # Zuordnung der SubTasks zum Task herstellen
        for sub_task_data in sub_tasks_data:
            SubTask.objects.create(parentTask=task, **sub_task_data)

        return task

    def update(self, instance, validated_data):
        # Extrahiere die verschachtelten Daten, falls vorhanden
        sub_tasks_data = validated_data.pop('subTasks', None)
        assigned_to_data = validated_data.pop('assignedTo', None)

        # Update der Standardfelder
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Aktualisiere die Many-to-Many-Beziehung:
        # Falls im Request übergeben, setze die Beziehung auf die neuen, existierenden Contact-IDs.
        if assigned_to_data is not None:
            instance.assignedTo.clear()
            # Extract IDs from contact objects and set the relationship
            contact_ids = [Contact.objects.get(
                email=contact['email']).id for contact in assigned_to_data]
            instance.assignedTo.set(contact_ids)

        # Aktualisiere SubTasks:
        # Beispiel: Lösche alle bestehenden SubTasks und erstelle sie neu.
        if sub_tasks_data is not None:
            instance.subTasks.all().delete()
            for sub_task_data in sub_tasks_data:
                SubTask.objects.create(parentTask=instance, **sub_task_data)

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
