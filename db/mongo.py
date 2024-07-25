from pymongo import MongoClient

#MongoDB setup
client = MongoClient('mongodb://localhost:27107')
database_name = "sentiment_logs"

def create_database(client, db_name):
    db_list = client.list_database_names()

    if db_name not in db_list:
        db = client[db_name]
        log_collection = db.create_collection('api_log')
    else:
        print("Database {db_name} already exits")
        log_collection = db.api_log

    return log_collection

