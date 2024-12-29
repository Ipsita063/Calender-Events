from fastapi import APIRouter
from app.routers import events  # Import individual routers here

# Create a master router to include all sub-routers
api_router = APIRouter()

# Include sub-routers
api_router.include_router(events.router)
