from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import UserTwo


def delete_user_psql(user_id: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        user = db.query(UserTwo).filter(UserTwo.id == user_id).first()

        if not user:
            return {
                "message": "User not found",
                "status_code": 404
            }

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully from service_backend",
            "status_code": 200,
            "user_id": str(user_id)
        }

    except ValueError:
        return {
            "message": "Invalid UUID format",
            "status_code": 400
        }
    except Exception as e:
        db.rollback()
        return {
            "message": f"delete_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()
