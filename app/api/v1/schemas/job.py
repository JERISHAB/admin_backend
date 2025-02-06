from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

# Base class for job-related fields
class JobBase(BaseModel):
    title: str
    category: str
    experience_required: int
    status: str
    location: str
    timing: str
    about: str
    responsibilities: str

# Schema for creating a job post
class JobCreate(JobBase):
    pass

# Schema for updating a job post (make all fields optional)
class JobUpdate(JobBase):
    title: Optional[str]
    category: Optional[str]
    experience_required: Optional[int]
    status: Optional[str]
    location: Optional[str]
    timing: Optional[str]
    about: Optional[str]
    responsibilities: Optional[str]

# Response schema for returning job details
class JobResponse(JobBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True  # Ensures compatibility with SQLAlchemy models
        arbitrary_types_allowed = True  # Allows for using arbitrary types like SQLAlchemy models
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Custom formatting for datetime
        }

    @field_validator("id", mode="before")
    def convert_uuid_to_str(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value
    
    @field_validator("created_at","updated_at", mode="before")
    def convert_datetime_to_str(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value
    
