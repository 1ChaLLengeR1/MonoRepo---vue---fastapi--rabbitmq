from celery_app import celery_app
from repository.update import update_user_psql

@celery_app.task
def update_user_task(user_id: str, name: str = None, lastname: str = None, email: str = None, age: str = None, city: str = None):
    result = update_user_psql(user_id, name, lastname, email, age, city)
    return result