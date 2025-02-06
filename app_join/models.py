from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    state = models.BooleanField(default=False)
    prio = models.IntegerField(default=0)
    dueDate = models.DateField()
    category = models.CharField(max_length=200)
    checkedUsers = models.ManyToManyField('User', related_name='checkedTasks')

    def __str__(self):
        return self.title


class SubTask(models.Model):
    state = models.BooleanField(default=False)
    description = models.TextField()
    parentTask = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='subTasks')

    def __str__(self):
        return self.description


class Contact(models.Model):
    author = models.CharField(max_length=200)
    checkbox = models.BooleanField(default=False)
    color = models.IntegerField()
    email = models.EmailField()
    name = models.CharField(max_length=200)
    nameInitials = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name
