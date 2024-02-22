import os


broker_url = os.getenv("CELERY_BROKER_URL", "pyamqp://guest@rabbitmq//")

# Celery configuration settings
broker_url = "pyamqp://guest@rabbitmq//"
result_backend = "rpc://"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
enable_utc = True
imports = ("app.worker.tasks",)
result_backend = "db+sqlite:///results.sqlite"
