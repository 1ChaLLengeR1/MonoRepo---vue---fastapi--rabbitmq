from celery_app import celery_app
from repository.create import main_create_task_psql
from repository.delete import main_delete_user_psql
from messaging.publisher import publish_user_deleted


@celery_app.task(bind=True)
def main_delete_user_task(self, user_id: str):
    task_id = self.request.id
    main_create_task_psql(task_id, "RUNNING", f"Delete user with this id: {user_id}.")

    try:
        result = main_delete_user_psql(user_id)
        if result.get('status_code') == 200:
            main_create_task_psql(task_id, "SUCCESS", f"User delete successfully: {result.get('email')}")
            publish_user_deleted(result.get('email'))
        else:
            main_create_task_psql(task_id, "FAILURE", f"Delete user failed: {result.get('message')}")

        return result

    except Exception as e:
        main_create_task_psql(task_id, "FAILURE", f"Exception during delete user: {str(e)}")
        raise
