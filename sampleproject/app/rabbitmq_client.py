# # app/rabbitmq_client.py
# import pika
# import os
# from dotenv import load_dotenv

# load_dotenv()

# RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
# RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "sample_queue")

# def publish_message_to_rabbitmq(message: str):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
#     channel = connection.channel()

#     channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
#     channel.basic_publish(
#         exchange='',
#         routing_key=RABBITMQ_QUEUE,
#         body=message,
#         properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
#     )

#     connection.close()


# def consume_one_message_from_rabbitmq():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
#     channel = connection.channel()

#     method_frame, header_frame, body = channel.basic_get(queue=RABBITMQ_QUEUE, auto_ack=True)

#     connection.close()

#     if method_frame:
#         return body.decode()
#     else:
#         return None



# app/rabbitmq_client.py
import pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "sample_queue")

# credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
# parameters = pika.ConnectionParameters(
#     host=RABBITMQ_HOST,
#     port=RABBITMQ_PORT,
#     credentials=credentials
# )

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=credentials
)

def publish_message_to_rabbitmq(message: str):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()


def consume_one_message_from_rabbitmq():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    method_frame, header_frame, body = channel.basic_get(queue=RABBITMQ_QUEUE, auto_ack=True)

    connection.close()

    if method_frame:
        return body.decode()
    else:
        return None
