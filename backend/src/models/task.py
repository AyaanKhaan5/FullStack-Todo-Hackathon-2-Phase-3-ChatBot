"""Task model definition."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Each task belongs to exactly one user. All task operations must
    enforce user ownership to prevent cross-user data access.
    """
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        description="Unique task identifier (auto-increment)"
    )

    # Foreign key to User
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
        description="Owner user ID (foreign key to users.id)"
    )

    # Task content
    title: str = Field(
        nullable=False,
        min_length=1,
        max_length=500,
        description="Task title (required, 1-500 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task description (optional, max 5000 characters)"
    )

    # Task status
    is_completed: bool = Field(
        default=False,
        nullable=False,
        description="Task completion status (default: false)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when task was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when task was last updated"
    )
