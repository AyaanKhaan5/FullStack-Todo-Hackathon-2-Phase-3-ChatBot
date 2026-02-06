"""Chat request and response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language message"
    )
    conversation_id: Optional[uuid.UUID] = Field(
        default=None,
        description="Existing conversation ID, or null to start new conversation"
    )


class MessageResponse(BaseModel):
    """Message schema in response."""
    id: uuid.UUID = Field(description="Message UUID")
    role: str = Field(description="Message sender role (user or assistant)")
    content: str = Field(description="Message text content")
    created_at: datetime = Field(description="Message creation timestamp")

    class Config:
        from_attributes = True


class ActionResponse(BaseModel):
    """Action performed by the assistant."""
    type: str = Field(
        description="Type of action (task_created, task_updated, etc.)"
    )
    task_id: Optional[int] = Field(
        default=None,
        description="Task ID for single task actions"
    )
    task_ids: Optional[List[int]] = Field(
        default=None,
        description="Task IDs for list actions"
    )


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: uuid.UUID = Field(
        description="Conversation ID (new or existing)"
    )
    message: MessageResponse = Field(
        description="Assistant's response message"
    )
    actions: List[ActionResponse] = Field(
        default_factory=list,
        description="Actions performed by the assistant"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error code if operation failed gracefully"
    )
