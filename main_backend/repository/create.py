from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.model import UserOne
from database.model import TaskResult


def main_create_user_psql(name: str, lastname: str, email: str, age: str, city: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        new_user = UserOne(
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
            "message": "User created successfully",
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


def main_create_task_psql(task_id: str, status: str, result: str) -> dict:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        # Sprawdź czy task już istnieje
        existing_task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()

        if existing_task:
            # Aktualizuj istniejący task
            existing_task.status = status
            existing_task.result = result
            db.commit()
            db.refresh(existing_task)

            print({
                "message": "Task updated successfully",
                "status_code": 200,
            })
            return {
                "message": "Task updated successfully",
                "status_code": 200,
            }
        else:
            # Stwórz nowy task
            new_task = TaskResult(
                task_id=task_id,
                status=status,
                result=result,
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            print({
                "message": "Task updated successfully",
                "status_code": 200,
            })
            return {
                "message": "Task created successfully",
                "status_code": 201,
            }

    except Exception as e:
        db.rollback()
        return {
            "message": f"main_create_task_psql - Exception - {str(e)}",
            "status_code": 417
        }
    finally:
        db.close()
