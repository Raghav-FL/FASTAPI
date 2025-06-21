from fastapi import APIRouter, HTTPException
from .models import SampleItem
from .db import collection
from .utils import document_to_dict
from .redis_client import redis_client
from .postgres_db import database
import os
from .rabbitmq_client import publish_message_to_rabbitmq
from .rabbitmq_client import consume_one_message_from_rabbitmq
from .rabbitmq_client import parameters
router = APIRouter()
import pika
import requests

@router.post("/mongo-insert", summary="Insert a document into MongoDB and Redis")
async def insert_item(item: SampleItem):
    result = await collection.insert_one(item.dict())
    mongo_id = str(result.inserted_id)

    redis_key = os.getenv("REDIS_SAMPLE_KEY", "sample_key")
    redis_client.set(redis_key, f"{item.name}:{item.value}")

    return {
        "message": "Item inserted",
        "inserted_id": mongo_id,
        "redis_key": redis_key,
        "redis_value": f"{item.name}:{item.value}"
    }

@router.get("/mongo-document-get", summary="Get all documents from MongoDB")
async def get_all_items():
    items = []
    cursor = collection.find({})
    async for document in cursor:
        items.append(document_to_dict(document))
    return items

@router.get("/redis-ping")
def redis_ping():
    try:
        pong = redis_client.ping()
        return {"redis": "pong" if pong else "no response"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/redis-document-get", summary="Get saved document from Redis")
async def get_redis_document():
    redis_key = os.getenv("REDIS_SAMPLE_KEY", "sample_key")
    value = redis_client.get(redis_key)
    if value:
        return {"redis_key": redis_key, "redis_value": value}
    return {"redis_key": redis_key, "message": "No value found in Redis"}

@router.post("/postgres-insert", summary="Insert document content into PostgreSQL")
async def postgres_insert(item: SampleItem):
    query = "INSERT INTO documents (content) VALUES (:content) RETURNING id"
    values = {"content": f"{item.name}:{item.value}"}
    try:
        inserted_id = await database.execute(query=query, values=values)
        return {"message": "Document inserted into PostgreSQL", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/postgres-documents", summary="Get all documents from PostgreSQL")
async def postgres_get_all():
    query = "SELECT id, content FROM documents"
    try:
        rows = await database.fetch_all(query=query)
        return [{"id": row["id"], "content": row["content"]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





from .rabbitmq_client import publish_message_to_rabbitmq

@router.post("/rabbit-publish", summary="Publish a message to RabbitMQ")
async def publish_to_rabbitmq(item: SampleItem):
    message = f"{item.name}:{item.value}"
    try:
        publish_message_to_rabbitmq(message)
        return {"message": "Published to RabbitMQ", "payload": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish: {str(e)}")




@router.get("/rabbit-consume", summary="Consume one message from RabbitMQ")
async def consume_message():
    try:
        message = consume_one_message_from_rabbitmq()
        if message:
            return {"message": message}
        else:
            raise HTTPException(status_code=404, detail="No messages in queue")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consuming message: {str(e)}")




@router.get("/rabbitmq-health", summary="Check RabbitMQ connection health")
def rabbitmq_health_check():
    try:
        connection = pika.BlockingConnection(parameters)
        if connection.is_open:
            connection.close()
            return {"status": "healthy", "message": "Connected to RabbitMQ successfully"}
        else:
            return {"status": "unhealthy", "message": "Connection to RabbitMQ is not open"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RabbitMQ connection failed: {str(e)}")


@router.get("/rabbitmq-logs", summary="Fetch recent RabbitMQ logs (via management API)")
def rabbitmq_logs():
    mgmt_host = os.getenv("RABBITMQ_MANAGEMENT_HOST", "localhost")
    mgmt_port = int(os.getenv("RABBITMQ_MANAGEMENT_PORT", 15672))
    mgmt_user = os.getenv("RABBITMQ_MANAGEMENT_USER", "guest")
    mgmt_pass = os.getenv("RABBITMQ_MANAGEMENT_PASS", "guest")

    url = f"http://{mgmt_host}:{mgmt_port}/api/logs"  # Note: RabbitMQ management API does not provide logs directly
    # The API doesn't provide logs directly, but you can get server info or events.

    # For demonstration, let's get overview info (health, nodes, queues)
    overview_url = f"http://{mgmt_host}:{mgmt_port}/api/overview"

    try:
        response = requests.get(overview_url, auth=(mgmt_user, mgmt_pass), timeout=5)
        response.raise_for_status()
        data = response.json()
        return {"overview": data}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch RabbitMQ overview: {str(e)}")
