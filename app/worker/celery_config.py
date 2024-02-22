from kombu import Exchange, Queue

broker_url = 'amqp://guest:guest@localhost:5672//'
task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('stripe_tasks', Exchange('stripe_tasks'), routing_key='stripe_tasks'),
)
task_default_queue = 'default'
task_default_exchange = 'default'
task_default_routing_key = 'default'