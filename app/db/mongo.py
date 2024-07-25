from pymongo import MongoClient

#MongoDB setup
client = MongoClient('mongodb://localhost:27107')
database_name = "sentiment_logs"
collection_name = "api_logs"

def get_database_and_collection(client, db_name, collection_name):
    db_list = client.list_database_names()
    if db_name not in db_list:
        db = client[db_name]
        db.create_collection(collection_name)
        print(f"Database {db_name} and collection {collection_name} created")
    else:
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection {collection_name} created in database {database}")
        
    return db[collection_name]

logs_collection = get_database_and_collection(client, db_name, collection_name)

def log_to_mongo(log_entry):
    try:
        logs_collection.insert_one(log_entry)
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