from repository.one import one_user_psql

def handler_one_user(user_id: str) -> dict:
    try:
        result = one_user_psql(user_id)
        return result
    except Exception as e:
        return {
            "message": f"handler_one_user - Exception - {str(e)}",
            "status_code": 500
        }
