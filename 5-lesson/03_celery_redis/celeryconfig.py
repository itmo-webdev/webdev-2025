from celery.schedules import crontab

# Конфигурация для периодических задач Celery Beat
beat_schedule = {
    # Отправка отчета каждую минуту
    'minute-report': {
        'task': 'tasks.send_email_task',
        'schedule': crontab(minute=0),
        'args': ('admin@example.com', 'Минутный отчет', 'Отчет за последнюю минуту')
    },
    # Отправка отчета каждый день в 9:00
    'daily-report': {
        'task': 'tasks.send_email_task',
        'schedule': crontab(hour=9, minute=0),
        'args': ('admin@example.com', 'Ежедневный отчет', 'Отчет за вчерашний день')
    },
    
    # Отправка напоминания каждый час
    'hourly-reminder': {
        'task': 'tasks.send_email_task',
        'schedule': crontab(minute=0),  # Каждый час в начале часа
        'args': ('team@example.com', 'Почасовое напоминание', 'Проверьте систему')
    },
    
    # Еженедельный отчет по понедельникам в 10:00
    'weekly-report': {
        'task': 'tasks.send_email_task',
        'schedule': crontab(hour=10, minute=0, day_of_week=1),
        'args': ('boss@example.com', 'Еженедельный отчет', 'Отчет за прошлую неделю')
    },
}

# Часовой пояс для Celery Beat
timezone = 'Europe/Moscow'

# Дополнительные настройки
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True

