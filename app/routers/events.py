from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.schemas.events import EventCreate, EventResponse, FilterParams
from app.models.event import Event
from app.utils.dependencies import get_db
from app.utils.validators import validate_time_range, validate_time_format, check_event_exists
from app.utils.formatter import format_datetime
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event in the calendar.
    """
    # Validate the time format of the event
    try:
        event_time = validate_time_format(event.time, "%Y-%m-%dT%H:%M:%S")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid time format: {str(e)}")

    # Check if the event with the same ID already exists
    existing_event = check_event_exists(event.id, db)
    if existing_event:
        raise HTTPException(
            status_code=409,  # Conflict: Event with the same ID exists
            detail=f"An event with ID {event.id} already exists. Please use a unique ID."
        )

    # Create and store the new event
    db_event = Event(description=event.description, time=event_time, id=event.id)

    try:
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
    except SQLAlchemyError as e:
        db.rollback()  # Rollback on DB-related errors
        raise HTTPException(status_code=500, detail=f"Database error occurred while creating a new event")

    return db_event

@router.get("/", response_model=List[EventResponse])
async def get_events(filter_params: FilterParams = Depends(), db: Session = Depends(get_db)):
    """
    Retrieve events with optional filters for time range and datetime formatting.
    """
    try:
        query = db.query(Event)

        # Apply filters for time range if provided
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid time format: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred while getting the event")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve events due to an unexpected error")

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single event by its ID.
    """
    try:
        db_event = db.query(Event).filter(Event.id == event_id).first()

        if not db_event:
            raise HTTPException(status_code=404, detail=f"No event found with ID {event_id}")

        return db_event
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve event due to an unexpected error")
