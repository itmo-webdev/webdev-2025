from celery import Celery
import time
from datetime import datetime

# Создаем экземпляр Celery
app = Celery(
    'email_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Конфигурация Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)


@app.task(name='tasks.send_email_task')
def send_email_task(to: str, subject: str, body: str):
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] CELERY: ОТПРАВКА EMAIL")
    print(f"{'='*60}")
    print(f"Кому: {to}")
    print(f"Тема: {subject}")
    print(f"Сообщение: {body}")
    print(f"{'='*60}\n")
    
    time.sleep(2)
    
    result = {
        "to": to,
        "subject": subject,
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }
    
    print(f"✓ Email успешно отправлен на {to}\n")
    
    return result


@app.task(name='tasks.send_bulk_emails')
def send_bulk_emails(recipients: list, subject: str, body: str):
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] CELERY: МАССОВАЯ РАССЫЛКА")
    print(f"{'='*60}")
    print(f"Количество получателей: {len(recipients)}")
    print(f"Тема: {subject}")
    print(f"{'='*60}\n")
    
    results = []
    for recipient in recipients:
        time.sleep(0.5)
        print(f"  → Отправлено на {recipient}")
        results.append({
            "to": recipient,
            "status": "sent",
            "sent_at": datetime.now().isoformat()
        })
    
    print(f"\n✓ Массовая рассылка завершена: {len(results)} писем\n")
    
    return {
        "total": len(results),
        "results": results
    }


@app.task(name='tasks.with_retry', bind=True, max_retries=3)
def with_retry(self, x: int):
    try:
        result = 100 / x
        return result
    except ZeroDivisionError as exc:
        retry_count = self.request.retries
        countdown = 10 * (2 ** retry_count)
        
        raise self.retry(
            exc=exc,
            countdown=countdown,
            max_retries=3
        )

