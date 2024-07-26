from fastapi import FastAPI, HTTPException, Request
from .models import Review
from .services import make_predictions
from .db.mongo import log_to_mongo, create_log_entry, initalize_logs_collection, mongo_collection_name, mongo_db_name, mongo_uri
from .db.sql import push_to_postgres


app = FastAPI(title="IMDB Sentiment classifier API",
              version="0.2")

@app.on_event("startup")
async def startup_event():
    await initalize_logs_collection()

@app.post("/predict")
async def predict_sentiment(review: Review, request: Request):
    log_entry = create_log_entry(request, review.text, "received")
    try:
        try:
            result = make_predictions(review.text)
        except Exception as model_Exception:
            log_entry = create_log_entry(request, review.text, "Preidction Error", str(model_Exception))
            raise HTTPException(status_code=500, detail="Prediction error")

        try:
            push_to_postgres(review.text, result["Sentiment"], result["Probability"])
        except Exception as database_Exception:
            log_entry = create_log_entry(request, review.text, "Database Error", str(database_Exception))
            raise HTTPException(status_code=500, detail="Database error")
        
        log_entry = create_log_entry(request, review.text, "success")
        return result
    
    except Exception as general_Exception:
        print(general_Exception)
        log_entry = create_log_entry(request, review.text, "general Error", str(general_Exception))
        raise HTTPException(status_code=500, detail="An unexpected error occured")
    
    finally:
        await log_to_mongo(log_entry)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)