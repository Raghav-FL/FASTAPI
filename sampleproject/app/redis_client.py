# import os
# import redis
# from dotenv import load_dotenv

# load_dotenv()

# REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
# REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_USERNAME = os.getenv("REDIS_USERNAME", None)   # Add this in your .env
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)   # Add this in your .env

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    decode_responses=True
)
