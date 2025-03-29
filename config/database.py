from pymongo import MongoClient
from config.settings import settings

client = None
db = None

def connect_db():
    global client, db
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    return db

def get_db():
    if client is None:
        connect_db()
    return db

def close_db():
    global client
    if client is not None:
        client.close()
        client = None