from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)