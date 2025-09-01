from celery_app import celery_app
from repository.delete import delete_user_psql
from messaging.publisher import publish_user_deleted

@celery_app.task
def delete_user_task(user_id: str):
    result = delete_user_psql(user_id)
    
    if result.get('status_code') == 200:
        publish_user_deleted(user_id)
    
    return result