@echo off
echo ========================================
echo Todo App - Запуск сервера
echo ========================================
echo.

echo Проверка установленных пакетов...
pip install -r requirements.txt

echo.
echo Создание миграций...
python manage.py makemigrations

echo.
echo Применение миграций...
python manage.py migrate

echo.
echo ========================================
echo Сервер запускается...
echo Откройте браузер: http://127.0.0.1:8000
echo ========================================
echo.
echo Для работы уведомлений также запустите:
echo 1. Redis сервер
echo 2. celery -A todo_project worker -l info --pool=solo
echo 3. celery -A todo_project beat -l info
echo.

python manage.py runserver
