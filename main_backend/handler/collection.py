from main_backend.repository.collection import collection_user_psql

def handler_collection_user() -> dict:
    try:
        result = collection_user_psql()
        return result
    except Exception as e:
        return {
            "message": f"handler_collection_user - Exception - {str(e)}",
            "status_code": 500
        }
