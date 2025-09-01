from database.db import get_db
from sqlalchemy.orm import Session
from service_backend.database.model import UserTwo


def one_user_psql(user_id: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        user = db.query(UserTwo).filter(UserTwo.id == user_id).first()
        
        if not user:
            return {
                "message": "User not found",
                "status_code": 404
            }
        
        return {
            "message": "User retrieved successfully from service_backend",
            "status_code": 200,
            "user": {
                "id": str(user.id),
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "age": user.age,
                "city": user.city
            }
        }

    except ValueError:
        return {
            "message": "Invalid UUID format",
            "status_code": 400
        }
    except Exception as e:
        return {
            "message": f"one_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()