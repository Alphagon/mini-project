from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/sentiment_db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

class Prediction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    review_text: str
    predicted_label: str
    probability: float

# Create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

asyncio.run(init_db())