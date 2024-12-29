from fastapi import FastAPI
from routers import api_router
import uvicorn

app = FastAPI(
    title="Calendar Events",
    version="1.0",
    description="Endpoints for managing the Calendar Events"
)

app.include_router(api_router, prefix="/events")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
