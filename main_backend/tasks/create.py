from celery_app import celery_app
from repository.create import main_create_user_psql, main_create_task_psql
from messaging.publisher import publish_user_created


@celery_app.task(bind=True)
def main_create_user_task(self, name: str, lastname: str, email: str, age: str, city: str):
    task_id = self.request.id
    main_create_task_psql(task_id, "RUNNING", f"Creating user: {name} {lastname}")
    try:
        result = main_create_user_psql(name, lastname, email, age, city)
        if result.get('status_code') == 201:
            main_create_task_psql(task_id, "SUCCESS", f"User created successfully: {result.get('user_id')}")

            user_data = {
                'id': result.get('user_id'),
                'name': name,
                'lastname': lastname,
                'email': email,
                'age': age,
                'city': city
            }
            publish_user_created(user_data)
        else:
            main_create_task_psql(task_id, "FAILURE", f"User creation failed: {result.get('message')}")

        return result

    except Exception as e:
        main_create_task_psql(task_id, "FAILURE", f"Exception during user creation: {str(e)}")
        raise
