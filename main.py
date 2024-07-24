# This is a branch push - test

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import load_model
from pymongo import MongoClient
import psycopg2
import json

#Parameters
max_len = 100
max_features = 10000

word_to_index = imdb.get_word_index()

model = load_model("sentiment-model.h5")

def preprocess_review(review, word_to_index, max_len, max_features):
    tokenizer = Tokenizer(num_words=max_features)
    tokenizer.word_index = word_to_index
    sequences = tokenizer.texts_to_sequences([review])
    padded_sequence = sequence.pad_sequences(sequences, maxlen=max_len)
    return padded_sequence

app = FastAPI(title="IMDB Sentiment classifier API",
              version="0.2")

class Review(BaseModel):
    text: str

# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')
db = client.sentiment_analysis
logs_collection = db.api_logs


# PostgreSQL setup
conn = psycopg2.connect(
    dbname="sentiment_db",
    user="need to update",
    password="same",
    host="postgres"
)
cursor = conn.cursor()

@app.post("/predict")
async def predict_sentiment(review: Review, request: Request):
    # Logging 
    log_entry = {
        "client": request.client.host,
        "review": review.text,
        "path": request.url.path,
        "method": request.method,
        "headers": dict(request.headers),
        "status": "received"
    }

    try:

        preprocessed_review = preprocess_review(review.text, word_to_index, max_len, max_features)

        try:
            prediction = model.predict(preprocessed_review)
        except Exception as model_Exception:
            log_entry["status"] = "Prediction error"
            log_entry["error_detail"] = str(model_Exception)
            raise HTTPException(status_code=500, detail="Prediction error")

        probability = prediction[0][0]
        predicted_label = (prediction > 0.5).astype("int32")

        sentiment = 'positive' if predicted_label[0][0] == 1 else 'negative'
        result = {"Sentiment": sentiment, "Probability": float(probability)}

        # Model input and output
        try:
            cursor.execute(
                "INSERT INTO predictions (review_text, predicted_label, probability) VALUES (%s, %s, %s)"
                (review.text, sentiment, probability)
            )
            conn.commit
        except Exception as db_Exception:
            log_entry["status"] = "Database Error"
            log_entry["error_detail"] = str(db_Exception)
            raise HTTPException(status_code=500, detail="Database error")
        
        log_entry["status"] = "success"
        logs_collection.insert_one(logs_collection)

        return result
    
    except Exception as general_Exception:
        log_entry["status"] = "General Error"
        log_entry["error_details"] = str(general_Exception)
        raise HTTPException(status_code=500, detail="An unexpected error occured")
    
    finally:
        logs_collection.insert_one(log_entry)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)