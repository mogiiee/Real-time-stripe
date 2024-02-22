# from confluent_kafka import Consumer
# import json
# from ..worker.tasks import create_stripe_customer, update_stripe_customer, delete_stripe_customer


# # Consumer configuration
# conf = {
#     'bootstrap.servers': "kafka:9092",
#     'group.id': "customer-group",
#     'auto.offset.reset': 'earliest'
# }

# consumer = Consumer(**conf)
# consumer.subscribe(['customer-create-topic', 'customer-update-topic', 'customer-delete-topic'])

# while True:
#     msg = consumer.poll(timeout=1.0)
#     if msg is None or msg.error():
#         continue
    
#     topic = msg.topic()
#     message_data = json.loads(msg.value().decode('utf-8'))
    
#     if topic == 'customer-create-topic':
#         create_stripe_customer(message_data)
#     elif topic == 'customer-update-topic':
#         update_stripe_customer(message_data['id'], message_data)
#     elif topic == 'customer-delete-topic':
#         delete_stripe_customer(message_data['id'])

# consumer.close()
