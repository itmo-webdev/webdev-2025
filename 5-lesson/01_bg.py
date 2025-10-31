from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from pydantic import BaseModel
from time import sleep
import random
app = FastAPI()


class User(BaseModel):
    name: str
    email: str
    password: str

def add_user(user: User):
    sleep(5)
    return random.randint(1, 1000000),

def send_notification(email: str):
    sleep(5)
    print(f"Notification sent to {email}")

@app.post("/add-user-legacy")
async def add_user_legacy(user: User):
    user_id = await add_user(user)
    send_notification(user.email)
    return { "id": str(user_id) }


@app.post("/add-user-bg")
async def add_user_bg(user: User, tasks: BackgroundTasks):
    user_id = await add_user(user)
    tasks.add_task(send_notification, user.email)
    return { "id": str(user_id) }


