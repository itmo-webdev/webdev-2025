#!/usr/bin/env python3
"""
Email Worker - слушает очередь и выполняет задачи по отправке email
"""

from redis import Redis
from rq import Worker, Queue

def main():
    # Подключение к Redis
    redis_conn = Redis(host='localhost', port=6379, db=0)
    
    # Создаем очередь
    queue = Queue('emails', connection=redis_conn)
    
    print("=" * 60)
    print("EMAIL WORKER ЗАПУЩЕН")
    print("=" * 60)
    print(f"Слушаю очередь: {queue.name}")
    print(f"Redis: localhost:6379")
    print("Нажмите Ctrl+C для остановки\n")
    
    # Создаем и запускаем worker
    worker = Worker([queue], connection=redis_conn)
    worker.work()


if __name__ == "__main__":
    main()

