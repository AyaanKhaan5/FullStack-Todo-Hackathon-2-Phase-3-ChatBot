"""User model definition."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    """
    User entity representing an authenticated user account.

    Each user can own multiple tasks. User authentication uses email/password
    with bcrypt hashing and JWT tokens.
    """
    __tablename__ = "users"

    # Primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="Unique user identifier (UUID v4)"
    )

    # User identification
    name: str = Field(
        nullable=False,
        max_length=255,
        description="User's full name"
    )

    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=255,
        description="User email address (unique, used for authentication)"
    )

    # Authentication
    hashed_password: str = Field(
        nullable=False,
        description="Bcrypt hashed password"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user account was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user account was last updated"
    )
