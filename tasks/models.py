from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Task(models.Model):
    """Модель задачи с дедлайном и статусом"""

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='Приоритет')
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    notification_sent = models.BooleanField(default=False, verbose_name='Уведомление отправлено')

    class Meta:
        ordering = ['deadline', '-priority']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    def get_color_class(self):
        """
        Возвращает класс цвета в зависимости от статуса и дедлайна:
        - Зеленый: задача завершена
        - Красный: дедлайн истек
        - Желтый: задача в процессе / осталось мало времени
        - Белый: обычная задача в ожидании
        """
        if self.status == 'completed':
            return 'success'  # Зеленый

        now = timezone.now()
        time_left = self.deadline - now

        if time_left.total_seconds() < 0:
            return 'danger'  # Красный - дедлайн истек
        elif time_left <= timedelta(days=1):
            return 'warning'  # Желтый - осталось меньше суток
        elif self.status == 'in_progress':
            return 'info'  # Голубой - в процессе
        else:
            return 'light'  # Светлый - обычная задача

    def is_overdue(self):
        """Проверяет, истек ли дедлайн"""
        if self.status == 'completed':
            return False
        return timezone.now() > self.deadline

    def time_until_deadline(self):
        """Возвращает время до дедлайна"""
        if self.status == 'completed':
            return None

        now = timezone.now()
        time_left = self.deadline - now

        if time_left.total_seconds() < 0:
            return "Просрочено"

        days = time_left.days
        hours = time_left.seconds // 3600
        minutes = (time_left.seconds % 3600) // 60

        if days > 0:
            return f"{days} д. {hours} ч."
        elif hours > 0:
            return f"{hours} ч. {minutes} мин."
        else:
            return f"{minutes} мин."

    def should_send_notification(self):
        """Проверяет, нужно ли отправить уведомление"""
        if self.notification_sent or self.status == 'completed':
            return False

        now = timezone.now()
        time_left = self.deadline - now

        # Отправить уведомление за 1 час до дедлайна или если дедлайн прошел
        return time_left <= timedelta(hours=1) or time_left.total_seconds() < 0
