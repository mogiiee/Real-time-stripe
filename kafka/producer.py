from confluent_kafka import Producer


conf = {'bootstrap.servers': "localhost:9092"}
producer = Producer(**conf)

def enqueue_customer_create(customer_data):
    producer.produce('customer-create-topic', key=str(customer_data['id']), value=str(customer_data))
    producer.flush()

def enqueue_customer_update(customer_id, customer_data):
    producer.produce('customer-update-topic', key=str(customer_id), value=str(customer_data))
    producer.flush()

def enqueue_customer_delete(customer_id):
    producer.produce('customer-delete-topic', key=str(customer_id), value=str(customer_id))
    producer.flush()
