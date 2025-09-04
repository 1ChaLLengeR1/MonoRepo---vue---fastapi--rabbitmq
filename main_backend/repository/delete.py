from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import UserOne


def main_delete_user_psql(user_id: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        user = db.query(UserOne).filter(UserOne.id == user_id).first()
        if not user:
            return {
                "message": "User not found",
                "status_code": 404
            }

        user_email = user.email

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully",
            "status_code": 200,
            "email": str(user_email)
        }

    except IntegrityError as e:
        db.rollback()
        return {
            "message": f"delete_user_psql - IntegrityError - {str(e)}",
            "status_code": 409
        }
    except Exception as e:
        db.rollback()
        return {
            "message": f"delete_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()
