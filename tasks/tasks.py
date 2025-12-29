"""
Celery tasks для отправки email уведомлений
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Task


@shared_task
def check_and_send_deadline_notifications():
    """
    Периодическая задача для проверки дедлайнов и отправки уведомлений
    Запускается каждые 30 минут
    """
    # Найти все задачи, по которым нужно отправить уведомление
    tasks = Task.objects.filter(
        status__in=['pending', 'in_progress'],
        notification_sent=False
    )

    notifications_sent = 0

    for task in tasks:
        if task.should_send_notification():
            send_deadline_notification.delay(task.id)
            notifications_sent += 1

    return f'Проверено задач: {tasks.count()}, отправлено уведомлений: {notifications_sent}'


@shared_task
def send_deadline_notification(task_id):
    """
    Отправка email уведомления о приближающемся дедлайне
    """
    try:
        task = Task.objects.get(id=task_id)

        # Проверяем, не отправлено ли уже уведомление
        if task.notification_sent or task.status == 'completed':
            return f'Уведомление для задачи {task.id} уже отправлено или задача завершена'

        user = task.user
        time_left = task.time_until_deadline()

        # Формируем тему письма
        if task.is_overdue():
            subject = f'⚠️ Дедлайн задачи "{task.title}" истек!'
        else:
            subject = f'⏰ Напоминание: дедлайн задачи "{task.title}" скоро истекает'

        # Формируем текст письма
        message = f"""
Здравствуйте, {user.username}!

Это автоматическое напоминание о задаче:

Название: {task.title}
Описание: {task.description or 'Не указано'}
Статус: {task.get_status_display()}
Приоритет: {task.get_priority_display()}
Дедлайн: {task.deadline.strftime('%d.%m.%Y %H:%M')}
Осталось времени: {time_left}

{'⚠️ Дедлайн уже истек! Пожалуйста, завершите задачу как можно скорее.' if task.is_overdue() else '⏰ До дедлайна осталось совсем немного времени.'}

Не забудьте завершить задачу вовремя!

---
С уважением,
Система управления задачами
"""

        # Отправка email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Отмечаем, что уведомление отправлено
        task.notification_sent = True
        task.save()

        return f'Уведомление для задачи {task.id} успешно отправлено на {user.email}'

    except Task.DoesNotExist:
        return f'Задача с ID {task_id} не найдена'
    except Exception as e:
        return f'Ошибка при отправке уведомления для задачи {task_id}: {str(e)}'
