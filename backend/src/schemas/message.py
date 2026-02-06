"""Message schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class MessageSchema(BaseModel):
    """Message schema."""
    id: uuid.UUID = Field(description="Message UUID")
    role: str = Field(description="Message sender role")
    content: str = Field(description="Message text content")
    created_at: datetime = Field(description="Message creation timestamp")

    class Config:
        from_attributes = True
