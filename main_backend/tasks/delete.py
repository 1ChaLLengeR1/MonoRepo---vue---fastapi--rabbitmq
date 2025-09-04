from celery_app import celery_app
from repository.delete import main_delete_user_psql
from messaging.publisher import publish_user_deleted

@celery_app.task
def main_delete_user_task(user_id: str):
    result = main_delete_user_psql(user_id)
    
    if result.get('status_code') == 200:
        publish_user_deleted(result.get('email'))
    
    return result