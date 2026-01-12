from celery import Celery

def make_celery():
    celery = Celery(
        "support_assistant",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True
    )

    return celery


celery_app = make_celery()
