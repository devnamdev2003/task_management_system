from django.contrib import admin
from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'start_date', 'end_date', 'priority')
    list_filter = ('category', 'priority')
    search_fields = ('name', 'category__name', 'description', 'location', 'organizer')
