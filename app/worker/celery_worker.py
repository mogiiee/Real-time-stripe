from celery import Celery

# Import the Celery configuration file
app = Celery("worker_app")
app.config_from_object("app.worker.celery_config")

# Import the tasks so Celery knows about them
from app.worker import tasks  # This will register the tasks with the Celery worker
