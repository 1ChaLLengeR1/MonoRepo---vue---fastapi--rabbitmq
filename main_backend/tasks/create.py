from celery_app import celery_app
from repository.create import main_create_user_psql
from messaging.publisher import publish_user_created


@celery_app.task
def main_create_user_task(name: str, lastname: str, email: str, age: str, city: str):
    result = main_create_user_psql(name, lastname, email, age, city)
    
    if result.get('status_code') == 201:
        user_data = {
            'id': result.get('user_id'),
            'name': name,
            'lastname': lastname,
            'email': email,
            'age': age,
            'city': city
        }
        publish_user_created(user_data)
    
    return result