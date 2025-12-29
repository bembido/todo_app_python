"""
Конфигурация периодических задач Celery
"""
from celery.schedules import crontab

# Настройка периодических задач
beat_schedule = {
    'check-deadlines-every-30-minutes': {
        'task': 'tasks.tasks.check_and_send_deadline_notifications',
        'schedule': crontab(minute='*/30'),  # Каждые 30 минут
    },
}
