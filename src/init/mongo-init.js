use sentiment_logs;

if (db.getCollectionNmaes().indexOf("api_logs") == -1) {
    db.createCollection("api_logs");
} else {
    print("Collection api_logs already exists")
}