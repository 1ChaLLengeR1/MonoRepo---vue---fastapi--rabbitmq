from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import UserOne


async def collection_user_psql() -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        users = db.query(UserOne).all()
        users_list = [
            {
                "id": str(user.id),
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "age": user.age,
                "city": user.city
            }
            for user in users
        ]
        
        return {
            "message": "Users retrieved successfully",
            "status_code": 200,
            "users": users_list,
            "count": len(users_list)
        }

    except IntegrityError as e:
        db.rollback()
        return {
            "message": f"collection_user_psql - IntegrityError - {str(e)}",
            "status_code": 409
        }
    except Exception as e:
        db.rollback()
        return {
            "message": f"collection_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()
