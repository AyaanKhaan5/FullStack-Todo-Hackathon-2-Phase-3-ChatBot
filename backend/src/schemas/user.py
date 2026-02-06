"""User Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from datetime import datetime
import uuid


class UserResponse(BaseModel):
    """Response schema for user data."""
    id: uuid.UUID
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM model conversion
