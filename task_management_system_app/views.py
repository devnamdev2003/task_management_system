from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Category, Task
from django.shortcuts import render, redirect
from .models import Category

from .models import Task
from django.urls import reverse


def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect(reverse('category_list'))


def create_task(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')

        # Retrieve the Category object
        category = Category.objects.get(pk=category_id)

        # Create the task object
        task = Task.objects.create(
            name=name,
            category=category,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            description=description,
            location=location,
            organizer=organizer
        )

        # Redirect to the task list page
        return redirect('category_list')
    else:
        categories = Category.objects.all()
        return render(request, 'task_management_system_app/create_task.html', {'categories': categories})


def update_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        # Update task fields based on form data
        task.name = request.POST.get('name')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        task.priority = request.POST.get('priority')
        task.description = request.POST.get('description')
        task.location = request.POST.get('location')
        task.organizer = request.POST.get('organizer')
        task.save()
        return redirect('category_list')
    else:
        # Render update task page with task data
        return render(request, 'task_management_system_app/update_task.html', {'task': task})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'task_management_system_app/category_list.html', {'categories': categories})


def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'task_management_system_app/create_category.html')


def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if category.task_set.exists():
        messages.error(
            request, "You cannot delete this category as it contains tasks.")
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")
    return redirect('category_list')


def category_tasks(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.task_set.all()
    return render(request, 'task_management_system_app/category_tasks.html', {'category': category, 'tasks': tasks})


def task_chart(request):
    categories = Category.objects.all()
    pending_counts = {}
    for category in categories:
        pending_counts[category.name] = Task.objects.filter(
            category=category,
            start_date__gt=timezone.now() 
        ).count()
    return render(request, 'task_management_system_app/task_chart.html', {'pending_counts': pending_counts})
