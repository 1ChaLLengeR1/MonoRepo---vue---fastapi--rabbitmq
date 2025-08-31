from celery_app import celery_app
from repository.delete import delete_user_psql

@celery_app.task
def delete_user_task(user_id: str):
    result = delete_user_psql(user_id)
    return result