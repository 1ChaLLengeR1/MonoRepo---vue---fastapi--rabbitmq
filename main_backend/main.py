from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from celery_app import celery_app
from handler.create import handler_create_user
from handler.collection import handler_collection_user, handler_collection_tasks
from handler.delete import handler_delete_user
from handler.update import handler_update_user

origins = [
    "http://localhost:5173",
]

# Tworzymy aplikację FastAPI
app_main = FastAPI()

app_main.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    result = await handler_create_user(user.name, user.lastname, user.email, user.age, user.city)
    return result


@app_main.get("/users/collection")
async def collection_user():
    result = await handler_collection_user()
    return result


@app_main.get("/tasks/collection")
async def collection_tasks():
    result = await handler_collection_tasks()
    return result


@app_main.patch("/users/update/{user_id}")
async def update_user(user: UserCreate, user_id: str):
    result = await handler_update_user(user_id, user.name, user.lastname, user.email, user.age, user.city)
    return result


@app_main.delete("/users/delete/{user_id}")
async def delete_user(user_id: str):
    result = await handler_delete_user(user_id)
    return result


@app_main.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result
    }
