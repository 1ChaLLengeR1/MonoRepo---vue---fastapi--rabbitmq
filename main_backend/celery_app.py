from celery import Celery

celery_app = Celery(
    'main_backend',
    backend="redis://redis:6379/0",              # nazwa serwisu redis
    broker="pyamqp://guest:guest@rabbitmq:5672//"  # nazwa serwisu rabbitmq
)

celery_app.autodiscover_tasks([
    'tasks.create',
    'tasks.delete',
    'tasks.update'
], force=True)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    imports=(
        'tasks.create',
        'tasks.delete',
        'tasks.update'
    ),
    accept_content=["json"],
    timezone="Europe/Warsaw",
    enable_utc=True,
)

from tasks import create, update, delete
