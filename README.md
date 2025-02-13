# Join Backend - Project Documentation

## Table of Contents

1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Models](#models)
4. [Serializers](#serializers)
5. [API Endpoints](#api-endpoints)
6. [Installation](#installation)
7. [Development Recommendations](#development-recommendations)

## Overview

Join Backend is a Django-based REST API system for managing tasks, contacts, and users. The project uses Django REST Framework for API implementation and supports CORS for frontend communication.

## Technology Stack

- Django 5.1.6
- Django REST Framework 3.15.2
- Django CORS Headers 4.6.0
- SQLite Database

## Models

### Task Model

A Task represents a main task in the system.

**Fields:**

- `title`: Title of the task (CharField)
- `description`: Description of the task (TextField)
- `state`: Status of the task (CharField)
- `prio`: Priority of the task (CharField)
- `dueDate`: Due date (DateField)
- `category`: Category of the task (CharField)
- `assignedTo`: ManyToMany relationship with contacts

### SubTask Model

SubTasks are subtasks associated with a main task.

**Fields:**

- `state`: Status of the subtask (BooleanField)
- `description`: Description of the subtask (TextField)
- `parentTask`: Link to the main task (ForeignKey)

### Contact Model

Manages contact information for people who can be assigned to tasks.

**Fields:**

- `author`: Name of the author (CharField)
- `checkbox`: Checkbox status (BooleanField)
- `color`: Color coding (IntegerField)
- `email`: Email address (EmailField)
- `name`: Name of the contact (CharField)
- `nameInitials`: Name initials (CharField)
- `phone`: Phone number (CharField)
- `assignedTo`: ManyToMany relationship with tasks

### User Model

Manages user information.

**Fields:**

- `email`: Email address (EmailField)
- `name`: Username (CharField)
- `password`: Password (CharField)

## Serializers

### TaskSerializer

Handles the serialization and deserialization of Task objects.

**Functionality:**

- Processes nested SubTasks
- Handles contact assignments
- Supports creating and updating tasks with associated SubTasks
- Validates incoming data
- Ensures relationships are properly stored

### SubTaskSerializer

Handles the serialization of subtasks.

**Functionality:**

- Serializes SubTask fields
- Validates SubTask data
- Handles relationship with parent task

### ContactSerializer

Handles the serialization of contact data.

**Functionality:**

- Serializes contact information
- Validates contact data
- Handles relationships with tasks

### UserSerializer

Handles the serialization of user data.

**Functionality:**

- Serializes user information
- Validates user data
- Handles passwords (currently unencrypted)

## API Endpoints

The API is available under `/api/v1/` and provides the following endpoints:

- `/api/v1/tasks/` - CRUD operations for Tasks
- `/api/v1/subtasks/` - CRUD operations for SubTasks
- `/api/v1/contacts/` - CRUD operations for Contacts
- `/api/v1/users/` - CRUD operations for Users

## Installation

1. Create and activate virtual environment:

python -m venv venv
source venv/bin/activate

2. Install dependencies:

pip install -r requirements.txt

3. Run the development server:

python manage.py runserver
