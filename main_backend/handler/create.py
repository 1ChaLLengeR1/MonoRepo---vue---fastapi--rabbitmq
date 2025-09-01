from tasks.create import create_user_task


async def handler_create_user(name: str, lastname: str, email: str, age: str, city: str) -> dict:
    try:
        task = create_user_task.delay(name, lastname, email, age, city)
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
