from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    """Список всех задач пользователя"""
    tasks = Task.objects.filter(user=request.user)

    # Фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'status_filter': status_filter,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    """Создание новой задачи"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Задача успешно создана!')
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Создать'})


@login_required
def task_edit(request, pk):
    """Редактирование задачи"""
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Редактировать', 'task': task})


@login_required
def task_delete(request, pk):
    """Удаление задачи"""
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача удалена!')
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_status(request, pk):
    """Быстрое переключение статуса задачи (AJAX)"""
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()

            return JsonResponse({
                'success': True,
                'status': task.get_status_display(),
                'color_class': task.get_color_class(),
                'time_left': task.time_until_deadline()
            })

    return JsonResponse({'success': False}, status=400)


@login_required
def dashboard(request):
    """Дашборд со статистикой задач"""
    tasks = Task.objects.filter(user=request.user)

    stats = {
        'total': tasks.count(),
        'pending': tasks.filter(status='pending').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'completed': tasks.filter(status='completed').count(),
        'overdue': sum(1 for task in tasks if task.is_overdue()),
    }

    # Ближайшие задачи по дедлайну
    upcoming_tasks = tasks.filter(status__in=['pending', 'in_progress']).order_by('deadline')[:5]

    context = {
        'stats': stats,
        'upcoming_tasks': upcoming_tasks,
    }

    return render(request, 'tasks/dashboard.html', context)
