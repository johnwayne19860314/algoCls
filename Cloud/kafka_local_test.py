from kafka import KafkaProducer, KafkaConsumer
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Kafka broker and topic configurations
#KAFKA_BROKER = 'localhost:9093'

KAFKA_BROKER = 'test.kafka.intersoul.io:9094'
#KAFKA_BROKER = 'aa206faec67534d159e2841919223ea7-87675424.us-west-1.elb.amazonaws.com:9094'

TOPIC_NAME = 'match.created'

# JSON serializer for the producer
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Kafka Producer
def create_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=json_serializer
    )

# Kafka Consumer
def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        # group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def produce_messages(producer, messages):
    for key, message in messages.items():
        producer.send(TOPIC_NAME, key=key.encode('utf-8'), value=message)
        print(f"Produced: {message}")
    producer.flush()

def consume_messages(consumer):
    print("Starting consumer...")
    for message in consumer:
        print(f"Consumed: {message.value}")

if __name__ == "__main__":
    # Example messages to produce
    messages = {
        '1': {"order_id": 1, "order_ts": 1534772501276, "total_amount": 10.50, "customer_name": "Bob Smith"},
        '2': {"order_id": 2, "order_ts": 1534772605276, "total_amount": 3.32, "customer_name": "Sarah Black"},
        '3': {"order_id": 3, "order_ts": 1534772742276, "total_amount": 21.00, "customer_name": "Emma Turner"}
    }

    producer = create_producer()
    produce_messages(producer, messages)

    consumer = create_consumer()
    time.sleep(2)  # wait briefly before consuming
    consume_messages(consumer)