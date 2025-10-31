import time
from datetime import datetime


def send_email_task(to: str, subject: str, body: str):
    """
    Имитирует отправку email.
    Просто логирует информацию о задаче.
    """
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ОТПРАВКА EMAIL")
    print(f"{'='*60}")
    print(f"Кому: {to}")
    print(f"Тема: {subject}")
    print(f"Сообщение: {body}")
    print(f"{'='*60}\n")
    
    # Имитируем отправку email (2 секунды)
    time.sleep(2)
    
    result = {
        "to": to,
        "subject": subject,
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }
    
    print(f"✓ Email успешно отправлен на {to}\n")
    
    return result

