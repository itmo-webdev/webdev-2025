from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tasks import send_email_task, send_bulk_emails
from celery.result import AsyncResult
from tasks import app as celery_app

app = FastAPI(title="Email Producer with Celery")


class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str


class BulkEmailRequest(BaseModel):
    recipients: list[str]
    subject: str
    body: str


@app.post("/send-email")
async def send_email(email: EmailRequest):
    """
    Отправляет задачу на отправку email через Celery
    """
    try:
        task = send_email_task.delay(email.to, email.subject, email.body)
        
        return {
            "task_id": task.id,
            "message": "Email задача добавлена в очередь Celery",
            "status": "queued",
            "to": email.to
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/send-bulk")
async def send_bulk(email: BulkEmailRequest):
    """
    Отправляет задачу на массовую рассылку через Celery
    """
    try:
        task = send_bulk_emails.delay(email.recipients, email.subject, email.body)
        
        return {
            "task_id": task.id,
            "message": f"Задача массовой рассылки добавлена ({len(email.recipients)} получателей)",
            "status": "queued",
            "recipients_count": len(email.recipients)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/test-retry/{number}")
async def test_retry(number: int):
    """
    Тестирует задачу с exponential backoff retry.
    Используйте 0 чтобы вызвать ошибку и увидеть retry.
    """
    try:
        task = with_retry.delay(number)
        
        return {
            "task_id": task.id,
            "message": f"Задача запущена: 100 / {number}",
            "status": "queued",
            "info": "Если number=0, увидите retry с backoff: 10, 20, 40 сек"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Проверяет статус задачи Celery
    """
    try:
        task = AsyncResult(task_id, app=celery_app)
        
        response = {
            "task_id": task_id,
            "status": task.status,
            "ready": task.ready(),
        }
        
        if task.ready():
            if task.successful():
                response["result"] = task.result
            elif task.failed():
                response["error"] = str(task.info)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Task not found: {str(e)}")


def signal_handler(signum, frame):
    """
    Обработчик сигналов для graceful shutdown
    """
    signal_name = signal.Signals(signum).name
    print(f"\n{'='*60}")
    print(f"Получен сигнал {signal_name}")
    print("Graceful shutdown...")
    print('='*60)
    sys.exit(0)


if __name__ == "__main__":
    import uvicorn
    
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Запускаем с graceful shutdown
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info",
        timeout_keep_alive=5,
        timeout_graceful_shutdown=10  # Graceful shutdown timeout
    )

