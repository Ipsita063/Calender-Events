from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    description: str
    time: str = Field(..., description="Event time in ISO format")
    id: int

    @field_validator("time")
    def validate_time_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Time must be in the format '%Y-%m-%dT%H:%M:%S'")
        return value


class EventResponse(BaseModel):
    id: int
    description: str
    time: str

    class Config:
        from_attributes = True  # Makes Pydantic work with SQLAlchemy models

    @field_validator("time", mode="before")
    def format_time(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S")
        return value


class FilterParams(BaseModel):
    datetime_format: str = Field(default="%Y-%m-%dT%H:%M:%S", description="Event date time format")
    from_time: Optional[str] = Field(default=None, description="Start date")
    to_time: Optional[str] = Field(default=None, description="End date")

    @field_validator("from_time", "to_time", mode="before")
    def validate_filter_time_format(cls, value):
        if value:
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError("Time must be in the format '%Y-%m-%dT%H:%M:%S'")
        return value
