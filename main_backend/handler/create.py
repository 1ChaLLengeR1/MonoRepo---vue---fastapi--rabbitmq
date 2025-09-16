from repository.create import main_create_task_psql
from tasks.create import main_create_user_task


async def handler_create_user(name: str, lastname: str, email: str, age: str, city: str) -> dict:
    try:
        task = main_create_user_task.delay(name, lastname, email, age, city)

        # Zapisz task jako PENDING
        main_create_task_psql(task.id, "PENDING", f"Task created for user: {name} {lastname}")

        return {
            "message": "User creation task started",
            "status_code": 202,
            "task_id": task.id
        }
    except Exception as e:
        return {
            "message": f"handler_create_user - Exception - {str(e)}",
            "status_code": 500
        }
