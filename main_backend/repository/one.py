from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import UserOne


def one_user_psql(user_id: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        user = db.query(UserOne).filter(UserOne.id == user_id).first()
        if not user:
            return {
                "message": "User not found",
                "status_code": 404
            }
        
        return {
            "message": "User retrieved successfully",
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

    except IntegrityError as e:
        db.rollback()
        return {
            "message": f"one_user_psql - IntegrityError - {str(e)}",
            "status_code": 409
        }
    except Exception as e:
        db.rollback()
        return {
            "message": f"one_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()
