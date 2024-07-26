# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

#MongoDB setup
mongo_uri = os.getenv('MONGO_URL', 'mongodb://mongo:27017')
client = AsyncIOMotorClient(mongo_uri)
database_name = "sentiment_logs"
collection_name = "api_logs"

async def get_database_and_collection(client, db_name, collection_name):
    db_list = await client.list_database_names()
    if db_name not in db_list:
        db = client[db_name]
        await db.create_collection(collection_name)
        print(f"Database {db_name} and collection {collection_name} created")
    else:
        db = client[db_name]
        collection_list = await db.list_collection_names()
        if collection_name not in collection_list:
            await db.create_collection(collection_name)
            print(f"Collection {collection_name} created in database {db_name}")
        
    return db[collection_name]

logs_collection = get_database_and_collection(client, database_name, collection_name)

async def log_to_mongo(log_entry):
    try:
        await logs_collection.insert_one(log_entry)
    except Exception as mongoException:
        print(f"Error logging in Mongo: \n{mongoException}")

def create_log_entry(request, review_text, status, error_details=None):
    log_entry = {
        "client": request.client.host,
        "review": review_text,
        "path": request.url.path,
        "method": request.method,
        "headers": dict(request.headers),
        "status": status
    }
    if error_details:
        log_entry["error_details"] = error_details
    return log_entry