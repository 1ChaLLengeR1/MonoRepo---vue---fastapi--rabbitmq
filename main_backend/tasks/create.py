from celery_app import celery_app
from repository.create import create_user_psql


@celery_app.task
def create_user_task(name: str, lastname: str, email: str, age: str, city: str):
    result = create_user_psql(name, lastname, email, age, city)
    print(result)
    return result