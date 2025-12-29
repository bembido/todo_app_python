from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'priority', 'deadline', 'is_overdue', 'notification_sent']
    list_filter = ['status', 'priority', 'notification_sent', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'deadline'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'title', 'description')
        }),
        ('Статус и приоритет', {
            'fields': ('status', 'priority')
        }),
        ('Временные параметры', {
            'fields': ('deadline', 'created_at', 'updated_at')
        }),
        ('Уведомления', {
            'fields': ('notification_sent',)
        }),
    )
