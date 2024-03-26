import pytz
from datetime import datetime
import json
import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management_system.settings')

# Initialize Django
django.setup()

# Now you can import your models
from task_management_system_app.models import Category, Task
from django.contrib.auth.models import User

def import_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Create categories
    for category_data in data['categories']:
        category_name = category_data['name']
        category, created = Category.objects.get_or_create(name=category_name)

    # Create users and tasks
    for user_data in data['users']:
        username = user_data['username']
        user, created = User.objects.get_or_create(username=username)

        # Assign tasks to the user
        for task_data in user_data['tasks']:
            task_name = task_data['name']
            category_name = task_data['category']
            start_date_str = task_data['start_date']
            end_date_str = task_data['end_date']
            priority = task_data['priority']
            description = task_data['description']
            location = task_data.get('location', '')  # location is optional
            organizer = task_data.get('organizer', '')  # organizer is optional

            # Get or create the category
            category, created = Category.objects.get_or_create(name=category_name)

            # Parse datetime strings
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)

            # Create the task
            Task.objects.create(
                name=task_name,
                category=category,
                assigned_to=user,
                start_date=start_date,
                end_date=end_date,
                priority=priority,
                description=description,
                location=location,
                organizer=organizer
            )


if __name__ == "__main__":
    file_path = "./data.json"  # Update with your JSON file path
    import_data_from_json(file_path)
