# Generated by Django 5.1.6 on 2025-02-06 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('checkbox', models.BooleanField(default=False)),
                ('color', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=200)),
                ('nameInitials', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('state', models.BooleanField(default=False)),
                ('prio', models.IntegerField(default=0)),
                ('dueDate', models.DateField()),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('parentTask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subTasks', to='app_join.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='checkedUsers',
            field=models.ManyToManyField(related_name='checkedTasks', to='app_join.user'),
        ),
    ]
