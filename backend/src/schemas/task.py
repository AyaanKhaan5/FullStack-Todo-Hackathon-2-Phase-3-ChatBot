"""Task Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import uuid


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()


class TaskUpdate(BaseModel):
    """Request schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else v


class TaskComplete(BaseModel):
    """Request schema for toggling task completion."""
    is_completed: bool


class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: int
    user_id: uuid.UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM model conversion
