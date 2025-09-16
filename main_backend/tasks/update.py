from celery_app import celery_app
from repository.create import main_create_task_psql
from repository.update import main_update_user_psql
from messaging.publisher import publish_user_updated


@celery_app.task(bind=True)
def update_user_task(self, user_id: str, name: str = None, lastname: str = None, email: str = None, age: str = None,
                     city: str = None):
    task_id = self.request.id
    main_create_task_psql(task_id, "RUNNING", f"Update user with this id: {user_id}.")

    try:
        result = main_update_user_psql(user_id, name, lastname, email, age, city)
        if result.get('status_code') == 200:
            main_create_task_psql(task_id, "SUCCESS", f"User update successfully: {result.get('email')}")
            user_data = {
                'id': user_id,
                'name': name,
                'lastname': lastname,
                'email': email,
                'age': age,
                'city': city
            }
            publish_user_updated(user_data)
        else:
            main_create_task_psql(task_id, "FAILURE", f"Update user failed: {result.get('message')}")
        return result
    except Exception as e:
        main_create_task_psql(task_id, "FAILURE", f"Exception during update user: {str(e)}")
        raise
