"""Message model for chat messages."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid


class MessageRole(str, Enum):
    """Message sender role."""
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class Message(SQLModel, table=True):
    """
    Message entity representing a single chat message.

    Each message belongs to exactly one conversation and has a role
    (user or assistant) indicating the sender.
    """
    __tablename__ = "messages"

    # Primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique message identifier (UUID)"
    )

    # Foreign key to Conversation
    conversation_id: uuid.UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True,
        description="Parent conversation ID (foreign key to conversations.id)"
    )

    # Message content
    role: MessageRole = Field(
        nullable=False,
        description="Message sender role (user or assistant)"
    )

    content: str = Field(
        nullable=False,
        description="Message text content"
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp when message was created"
    )
