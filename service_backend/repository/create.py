from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from service_backend.database.model import UserTwo


def create_user_psql(name: str, lastname: str, email: str, age: str, city: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        new_user = UserTwo(
            name=name,
            lastname=lastname,
            email=email,
            age=age,
            city=city
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "message": "User created successfully in service_backend",
            "status_code": 201,
            "user_id": str(new_user.id)
        }

    except IntegrityError as e:
        db.rollback()
        return {
            "message": f"create_user_psql - IntegrityError - {str(e)}",
            "status_code": 409
        }
    except Exception as e:
        db.rollback()
        return {
            "message": f"create_user_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()