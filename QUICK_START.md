# Быстрый старт (без email уведомлений)

Если вы хотите быстро протестировать приложение без настройки Redis и Celery:

## 1. Временно отключите Celery

Откомментируйте импорт Celery в `todo_project/__init__.py`:

```python
# from .celery import app as celery_app
# __all__ = ('celery_app',)
```

## 2. Установите только Django

```bash
pip install Django==5.0.1
```

## 3. Выполните миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

## 5. Запустите сервер

```bash
python manage.py runserver
```

Откройте http://127.0.0.1:8000

## Ограничения без Celery

- ❌ Email уведомления НЕ будут работать
- ❌ Автоматическая проверка дедлайнов НЕ будет работать
- ✅ Все остальные функции работают полностью

## Для полной функциональности

Следуйте инструкциям в [README.md](README.md)
