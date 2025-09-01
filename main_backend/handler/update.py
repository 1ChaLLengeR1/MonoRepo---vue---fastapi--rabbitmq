from tasks.update import update_user_task

async def handler_update_user(user_id: str, name: str = None, lastname: str = None, email: str = None, age: str = None, city: str = None) -> dict:
    try:
        task = update_user_task.delay(user_id, name, lastname, email, age, city)
        
        return {
            "message": "User update task started",
            "status_code": 202,
            "task_id": task.id
        }
    except Exception as e:
        return {
            "message": f"handler_update_user - Exception - {str(e)}",
            "status_code": 500
        }
