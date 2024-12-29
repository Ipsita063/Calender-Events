from sqlalchemy.orm import Session
from app.database.connection import SessionLocal


def get_db() -> Session:
    """
    Dependency for getting a database session. Ensures that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
