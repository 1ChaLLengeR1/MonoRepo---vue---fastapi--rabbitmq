from celery_app import celery_app
from repository.update import update_user_psql
from messaging.publisher import publish_user_updated

@celery_app.task
def update_user_task(user_id: str, name: str = None, lastname: str = None, email: str = None, age: str = None, city: str = None):
    result = update_user_psql(user_id, name, lastname, email, age, city)
    
    if result.get('status_code') == 200:
        user_data = {
            'id': user_id,
            'name': name,
            'lastname': lastname,
            'email': email,
            'age': age,
            'city': city
        }
        publish_user_updated(user_data)
    
    return result