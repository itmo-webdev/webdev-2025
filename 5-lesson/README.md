# Email Worker (Celery + Redis)

## Выполнить
# Вкладка 1
redis-server

# Вкладка 2 (в уроке 5)
uvicorn app.main:app --reload --port 8000

# Вкладка 3 (в уроке 5)
python -m celery -A app.celery_app.celery worker --loglevel=info
# (необязательно) Воскресный календарь
python -m celery -A app.celery_app.celery beat --loglevel=info

## Тест
POST /news?title=Hello%20LMS
→ Записи в лог `email_worker.log`

## Выполнено
- Celery + Redis
- Повтор/откат/дрожание
- Идемпотентность (набор Redis)
- Ведение журнала в файлы