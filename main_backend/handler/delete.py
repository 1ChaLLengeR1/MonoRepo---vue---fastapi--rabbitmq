from tasks.delete import main_delete_user_task

async def handler_delete_user(user_id: str) -> dict:
    try:
        task = main_delete_user_task.delay(user_id)
        
        return {
            "message": "User deletion task started",
            "status_code": 202,
            "task_id": task.id
        }
    except Exception as e:
        return {
            "message": f"handler_delete_user - Exception - {str(e)}",
            "status_code": 500
        }
