from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.events import EventCreate, EventResponse, FilterParams
from app.models.event import Event
from app.utils.dependencies import get_db
from app.utils.validators import validate_time_range, validate_time_format
from app.utils.formatter import format_datetime
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event in the calendar.
    """
    try:
        # Check if the event ID already exists
        existing_event = db.query(Event).filter(Event.id == event.id).first()
        if existing_event:
            raise HTTPException(
                status_code=500,
                detail=f"An event with ID {event.id} already exists. Please use a unique ID.",
            )
        event_time = validate_time_format(event.time, "%Y-%m-%dT%H:%M:%S")
        db_event = Event(description=event.description, time=event_time, id=event.id)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")


@router.get("/", response_model=List[EventResponse])
async def get_events(filter_params: FilterParams = Depends(), db: Session = Depends(get_db)):
    """
    Retrieve events with optional filters for time range and datetime formatting.
    """
    try:
        query = db.query(Event)

        if filter_params.from_time and filter_params.to_time:
            validate_time_range(filter_params.from_time, filter_params.to_time)  # Utility function

        if filter_params.from_time:
            from_time = datetime.strptime(filter_params.from_time, filter_params.datetime_format)
            query = query.filter(Event.time >= from_time)

        if filter_params.to_time:
            to_time = datetime.strptime(filter_params.to_time, filter_params.datetime_format)
            query = query.filter(Event.time <= to_time)

        events = query.all()

        # Format the event time using a utility function
        for event in events:
            event.time = format_datetime(event.time, filter_params.datetime_format)

        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single event by its ID.
    """
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail=f"No Event Found With ID {event_id}")
    return db_event