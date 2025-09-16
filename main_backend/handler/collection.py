from repository.collection import main_collection_user_psql, main_collection_task_psql


async def handler_collection_user() -> dict:
    try:
        result = await main_collection_user_psql()
        return result
    except Exception as e:
        return {
            "message": f"handler_collection_user - Exception - {str(e)}",
            "status_code": 500
        }


async def handler_collection_tasks() -> dict:
    try:
        result = await main_collection_task_psql()
        return result
    except Exception as e:
        return {
            "message": f"handler_collection_tasks - Exception - {str(e)}",
            "status_code": 500
        }
