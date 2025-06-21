# import os
# from motor.motor_asyncio import AsyncIOMotorClient
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB = os.getenv("MONGO_DB")
# MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# client = AsyncIOMotorClient(MONGO_URI)
# db = client[MONGO_DB]
# collection = db[MONGO_COLLECTION]



import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?authSource=admin"

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
