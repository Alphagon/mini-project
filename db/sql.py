from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from sqlalchemy import Column, DateTime
from datetime import datetime

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/sentiment_db"
engine = create_engine(DATABASE_URL, echo=True, future=True)

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    review_text: str
    predicted_label: str
    probability: float
    timestamp: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))

# Create tables
SQLModel.metadata.create_all(engine)