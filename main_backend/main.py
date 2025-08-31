from fastapi import FastAPI
from pydantic import BaseModel
from celery_app import celery_app
from handler.create import handler_create_user
from repository.create import create_user_psql

# Tworzymy aplikację FastAPI
app_main = FastAPI()

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: str
    age: str
    city: str

# Prosty endpoint GET /hello
@app_main.get("/hello")
async def hello_world():
    return {"message": "Hello World main_backend"}

@app_main.post("/users")
async def create_user(user: UserCreate):
    # result = create_user_psql(user.name, user.lastname, user.email, user.age, user.city)
    result = await handler_create_user(user.name, user.lastname, user.email, user.age, user.city)
    return result

@app_main.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result
    }