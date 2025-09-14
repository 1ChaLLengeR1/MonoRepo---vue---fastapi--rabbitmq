from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import UserTwo


def update_user_psql(user_id: str, name: str = None, lastname: str = None, email: str = None, age: str = None,
                     city: str = None) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        user = db.query(UserTwo).filter(UserTwo.email == email).first()

        if not user:
            return {
                "message": f"User not found for this user_id: {user_id}",
                "status_code": 404
            }

        if name is not None:
            user.name = name
        if lastname is not None:
            user.lastname = lastname
        if email is not None:
            user.email = email
        if age is not None:
            user.age = age
        if city is not None:
            user.city = city

        db.commit()
        db.refresh(user)

        return {
            "message": "User updated successfully in service_backend",
            "status_code": 200,
            "email": str(user.email)
        }

    except ValueError:
        return {
            "message": "Invalid UUID format",
            "status_code": 400
        }
    except IntegrityError as e:
        db.rollback()
        return {
            "message": f"update_user_psql - IntegrityError - {str(e)}",
            "status_code": 409
        }
    except Exception as e:
        db.rollback()
        return {
            "message": f"update_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()
