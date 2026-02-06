"""Conversation model for chat sessions."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat session.

    Each conversation belongs to exactly one user. Conversations contain
    multiple messages and maintain chat history for context.
    """
    __tablename__ = "conversations"

    # Primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique conversation identifier (UUID)"
    )

    # Foreign key to User
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
        description="Owner user ID (foreign key to users.id)"
    )

    # Conversation metadata
    title: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Conversation title (auto-generated from first message)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp when conversation was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp when conversation was last updated"
    )
