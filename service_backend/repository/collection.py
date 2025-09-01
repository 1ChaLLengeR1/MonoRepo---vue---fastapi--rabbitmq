from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from service_backend.database.model import UserTwo


async def collection_user_psql() -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        users = db.query(UserTwo).all()
        
        users_list = []
        for user in users:
            users_list.append({
                "id": str(user.id),
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "age": user.age,
                "city": user.city
            })
        
        return {
            "message": "Users retrieved successfully from service_backend",
            "status_code": 200,
            "users": users_list,
            "count": len(users_list)
        }

    except Exception as e:
        return {
            "message": f"collection_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()