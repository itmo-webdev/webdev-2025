from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
from rq import Queue

app = FastAPI(title="Email Producer")

redis_conn = Redis(host='localhost', port=6379, db=0)
queue = Queue('emails', connection=redis_conn)


class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str


@app.post("/send-email")
async def send_email(email: EmailRequest):
    try:
        from tasks import send_email_task
        
        job = queue.enqueue(
            send_email_task,
            email.to,
            email.subject,
            email.body
        )
        
        return {
            "job_id": job.id,
            "message": f"Email задача добавлена в очередь",
            "status": "queued",
            "to": email.to
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

