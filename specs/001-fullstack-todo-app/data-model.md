# Data Model: Full-Stack Todo Web Application

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-08
**Status**: Complete

## Overview

This document defines the database schema and SQLModel entities for the Full-Stack Todo Web Application. The data model supports multi-user task management with strict user isolation and ownership enforcement.

---

## Entity Relationship Diagram

```text
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id: UUID (PK)       │
│ email: String       │
│ created_at: DateTime│
│ updated_at: DateTime│
└─────────────────────┘
          │
          │ 1
          │
          │ owns
          │
          │ *
          ▼
┌─────────────────────┐
│       Task          │
├─────────────────────┤
│ id: Integer (PK)    │
│ user_id: UUID (FK)  │
│ title: String       │
│ description: String │
│ is_completed: Bool  │
│ created_at: DateTime│
│ updated_at: DateTime│
└─────────────────────┘
```

**Relationship**: One User has many Tasks (1:N)

---

## Entity Definitions

### 1. User Entity

**Purpose**: Represents an authenticated user account in the system.

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """
    User entity representing an authenticated user account.

    Each user can own multiple tasks. User authentication is handled
    by Better Auth; this entity stores the user reference for task ownership.
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
    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=255,
        description="User email address (unique, used for authentication)"
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

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-08T10:00:00Z",
                "updated_at": "2026-01-08T10:00:00Z"
            }
        }
```

**Field Specifications**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, INDEXED | Unique identifier (auto-generated UUID v4) |
| `email` | String(255) | UNIQUE, NOT NULL, INDEXED | User email address for authentication |
| `created_at` | DateTime | NOT NULL, DEFAULT NOW() | Account creation timestamp (UTC) |
| `updated_at` | DateTime | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for fast lookup during authentication)

**Validation Rules**:
- Email must be valid format (validated by Better Auth before user creation)
- Email must be unique across all users
- Timestamps automatically set on creation and update

**Relationships**:
- One-to-many with Task entity (one user owns many tasks)

**Notes**:
- User creation is handled by Better Auth during authentication flow
- User deletion should cascade to delete all associated tasks (implement with ON DELETE CASCADE)
- `updated_at` should be automatically updated on any user record modification

---

### 2. Task Entity

**Purpose**: Represents a todo item owned by a specific user.

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Relationship
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
    id: int = Field(
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

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "is_completed": False,
                "created_at": "2026-01-08T10:00:00Z",
                "updated_at": "2026-01-08T10:00:00Z"
            }
        }
```

**Field Specifications**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner user reference |
| `title` | String(500) | NOT NULL, MIN_LENGTH 1, MAX_LENGTH 500 | Task title (required) |
| `description` | String(5000) | NULLABLE, MAX_LENGTH 5000 | Task description (optional) |
| `is_completed` | Boolean | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | DateTime | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |
| `updated_at` | DateTime | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` (for fast filtering by owner)
- Composite index on `(user_id, created_at)` (for sorted task lists)

**Validation Rules**:
- `title` must not be empty (min_length=1)
- `title` must not exceed 500 characters
- `description` must not exceed 5000 characters if provided
- `user_id` must reference an existing user
- `is_completed` defaults to False on creation
- `updated_at` automatically updated on any modification

**Relationships**:
- Many-to-one with User entity (many tasks belong to one user)
- Foreign key constraint with ON DELETE CASCADE (delete tasks when user deleted)

**Query Patterns**:

1. **List all tasks for a user** (most common):
   ```python
   tasks = session.exec(
       select(Task)
       .where(Task.user_id == user_id)
       .order_by(Task.created_at.desc())
   ).all()
   ```

2. **Get specific task with ownership check**:
   ```python
   task = session.exec(
       select(Task)
       .where(Task.id == task_id, Task.user_id == user_id)
   ).first()
   ```

3. **Count completed vs incomplete tasks**:
   ```python
   completed_count = session.exec(
       select(func.count(Task.id))
       .where(Task.user_id == user_id, Task.is_completed == True)
   ).one()
   ```

**State Transitions**:

```text
┌─────────────┐
│   Created   │ (is_completed = False)
│  (default)  │
└──────┬──────┘
       │
       │ PATCH /tasks/{id}/complete
       │ { is_completed: true }
       ▼
┌─────────────┐
│  Completed  │ (is_completed = True)
└──────┬──────┘
       │
       │ PATCH /tasks/{id}/complete
       │ { is_completed: false }
       ▼
┌─────────────┐
│   Created   │ (is_completed = False)
└─────────────┘
```

**Notes**:
- Tasks can be toggled between completed and incomplete states
- Deletion is permanent (no soft delete)
- All queries MUST filter by `user_id` to enforce ownership

---

## Database Schema (SQL DDL)

### PostgreSQL Schema

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index on email for fast authentication lookups
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL CHECK (LENGTH(title) > 0),
    description TEXT CHECK (LENGTH(description) <= 5000),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index on user_id for fast filtering
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Composite index for sorted task lists
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- Trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Pydantic Schemas (Request/Response)

### Task Schemas

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid

class TaskCreate(BaseModel):
    """Request schema for creating a new task"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)

    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

class TaskUpdate(BaseModel):
    """Request schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else v

class TaskComplete(BaseModel):
    """Request schema for toggling task completion"""
    is_completed: bool

class TaskResponse(BaseModel):
    """Response schema for task data"""
    id: int
    user_id: uuid.UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enable ORM model conversion
```

---

## Data Integrity Rules

### Referential Integrity

1. **User → Task Cascade Delete**
   - When a user is deleted, all their tasks are automatically deleted
   - Implemented via `ON DELETE CASCADE` foreign key constraint

2. **Task → User Reference**
   - Every task must reference a valid user
   - Cannot create task with non-existent user_id
   - Enforced by foreign key constraint

### Data Validation

1. **Title Validation**
   - Must not be empty (after trimming whitespace)
   - Must not exceed 500 characters
   - Enforced at database level (CHECK constraint) and application level (Pydantic)

2. **Description Validation**
   - Optional field (can be NULL)
   - Must not exceed 5000 characters if provided
   - Enforced at database level (CHECK constraint) and application level (Pydantic)

3. **Email Validation**
   - Must be unique across all users
   - Format validation handled by Better Auth before user creation
   - Uniqueness enforced by database UNIQUE constraint

### Timestamp Management

1. **Automatic Timestamps**
   - `created_at` set automatically on record creation
   - `updated_at` set automatically on record creation and update
   - Implemented via database triggers (PostgreSQL) or SQLModel defaults

2. **UTC Timezone**
   - All timestamps stored in UTC
   - Client applications responsible for timezone conversion

---

## Performance Considerations

### Index Strategy

1. **Primary Keys**: Automatic indexes on `users.id` and `tasks.id`
2. **Foreign Keys**: Index on `tasks.user_id` for fast joins and filtering
3. **Unique Constraints**: Index on `users.email` for authentication lookups
4. **Composite Index**: `(user_id, created_at)` for sorted task lists

### Query Optimization

1. **Task List Queries**: Use composite index for `WHERE user_id = ? ORDER BY created_at DESC`
2. **Task Ownership Checks**: Use indexed `user_id` for fast validation
3. **Connection Pooling**: Configured for 5 base + 10 overflow connections

### Scalability

- **Current Scale**: Supports 10,000 tasks per user, 100 concurrent users
- **Index Overhead**: Minimal with 3 indexes on tasks table
- **Growth Path**: Can add pagination for task lists if needed (LIMIT/OFFSET)

---

## Migration Strategy

### Initial Migration (Alembic)

```python
# alembic/versions/001_initial_schema.py
def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_user_created', 'tasks', ['user_id', 'created_at'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## Security Considerations

1. **User Isolation**: All task queries MUST include `WHERE user_id = ?` filter
2. **SQL Injection**: Prevented by SQLModel parameterized queries
3. **Cascade Deletion**: User deletion removes all tasks (prevents orphaned data)
4. **No Sensitive Data**: No passwords or secrets stored (handled by Better Auth)

---

## Summary

**Entities**: 2 (User, Task)
**Relationships**: 1 (User 1:N Task)
**Indexes**: 5 total (3 single-column, 1 composite, 1 unique)
**Constraints**: Foreign key with cascade delete, unique email, check constraints on title/description
**Validation**: Database-level + application-level (Pydantic)
**Performance**: Optimized for user-scoped queries with composite index
