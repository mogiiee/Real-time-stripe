

# Celery configuration settings
broker_url = 'pyamqp://guest@localhost//'
result_backend = 'rpc://'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/London'
enable_utc = True
imports = ('app.worker.tasks',)
result_backend = 'db+sqlite:///results.sqlite'
