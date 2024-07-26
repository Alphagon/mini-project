from sqlmodel import SQLModel, Field, create_engine, Session
# from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from sqlalchemy import Column, DateTime
from datetime import datetime
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path)

psql_username = os.getenv('POSTGRES_USERNAME')
psql_password = os.getenv('POSTGRES_PASSWORD')
psql_host = os.getenv('POSTGRES_HOST')
psql_port = os.getenv('POSTGRES_PORT')
psql_database_name = os.getenv("POSTGRES_DATABASE_NAME")

DATABASE_URL = f"postgresql://{psql_username}:{psql_password}@{psql_host}:{psql_port}/{psql_database_name}"
engine = create_engine(DATABASE_URL, echo=True, future=True)

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    review_text: str
    predicted_label: str
    probability: float
    timestamp: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))

# Create tables
SQLModel.metadata.create_all(engine)

def push_to_postgres(review, sentiment, probability):
    record = Prediction(review_text=review, predicted_label=sentiment, probability=round(float(probability), 2))
    with Session(engine) as session:
        session.add(record)
        session.commit()