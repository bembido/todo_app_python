// Главный JavaScript файл для Todo App

$(document).ready(function() {
    // Автоматическое скрытие сообщений через 5 секунд
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Обработка быстрого переключения статуса (если нужно)
    $('.status-toggle').on('click', function(e) {
        e.preventDefault();
        const taskId = $(this).data('task-id');
        const newStatus = $(this).data('status');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: `/task/${taskId}/toggle-status/`,
            method: 'POST',
            data: {
                status: newStatus,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                }
            },
            error: function() {
                alert('Ошибка при обновлении статуса');
            }
        });
    });

    // Подтверждение удаления
    $('.delete-confirm').on('click', function(e) {
        if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
            e.preventDefault();
        }
    });

    // Анимация появления карточек
    $('.card').each(function(index) {
        $(this).css('animation-delay', (index * 0.1) + 's');
        $(this).addClass('fade-in');
    });

    // Обновление времени до дедлайна каждую минуту
    setInterval(updateDeadlines, 60000);
});

function updateDeadlines() {
    // Можно добавить AJAX обновление времени до дедлайна
    console.log('Updating deadlines...');
}

// Функция для форматирования даты
function formatDate(date) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(date).toLocaleDateString('ru-RU', options);
}
