"""Conversation schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationSummary(BaseModel):
    """Conversation summary for list view."""
    id: uuid.UUID = Field(description="Conversation UUID")
    title: Optional[str] = Field(
        default=None,
        description="Conversation title (from first message)"
    )
    created_at: datetime = Field(description="Conversation creation timestamp")
    updated_at: datetime = Field(description="Last message timestamp")
    message_count: int = Field(description="Total number of messages")

    class Config:
        from_attributes = True
