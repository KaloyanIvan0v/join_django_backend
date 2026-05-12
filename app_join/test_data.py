user0 = {
    "display_name": "testuser",
    "email": "testy@mail.de",
    "password": "testpass123",
    "repeated_password": "testpass123"
}

user1 = {
    "display_name": "testuser1",
    "email": "testy1@mail.de",
    "password": "testpass123",
    "repeated_password": "testpass123"
}


contact = {
    "author": "contact_user1",
    "checkbox": False,
    "color": 1,
    "email": "contact1@mail.de",
    "name": "Contact 1",
    "nameInitials": "C1",
    "phone": "1234567890",
}

contactUpdate = {
    "author": "contact_user1",
    "checkbox": False,
    "color": 2,
    "email": "contact1@mail.de",
    "name": "Contact 1 Updated",
    "nameInitials": "CU",
    "phone": "9999999999",
}

taskInvalid = {
    "description": "Missing required fields.",
    "state": "To Do",
}

taskPatch = {
    "title": "Patched Title",
}

notExistingContact = {
    "id": 998,
    "author": "contact_user2",
    "checkbox": False,
    "color": 3,
    "email": "contact2@mail.de",
    "name": "Contact 2",
    "nameInitials": "C2",
    "phone": "1234567345345",
}


task = {
    "title": "Test Task",
    "description": "This is a test task.",
    "state": "To Do",
    "prio": "High",
    "dueDate": "2024-12-31",
    "category": "Testing",
}

taskWithNotExistingContact = {
    "title": "Test Task 2",
    "description": "This is another test task.",
    "state": "In Progress",
    "prio": "Medium",
    "dueDate": "2024-11-30",
    "category": "Testing",
    "assignedTo": [notExistingContact],
}
