from celery import Celery


celery_app = Celery(
    "main_backend",
    broker="pyamqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Warsaw",
    enable_utc=True,
)