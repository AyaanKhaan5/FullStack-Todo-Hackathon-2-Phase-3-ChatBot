# Data Model: AI-Powered Todo Chatbot with MCP

**Feature**: 003-ai-chatbot-mcp
**Date**: 2026-01-15
**Status**: Design Complete

## Overview

This document defines the database schema for Phase III AI chatbot functionality. New entities (Conversation, Message) integrate with existing Phase II entities (User, Task) without modifying existing schemas.

---

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │ (existing)
│  id: UUID   │
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       │ 1:N             │ 1:N
       ▼                 ▼
┌─────────────┐   ┌──────────────┐
│    Task     │   │ Conversation │ (new)
│  id: int    │   │  id: UUID    │
│  user_id    │   │  user_id     │
└─────────────┘   └──────┬───────┘
                         │
                         │ 1:N
                         ▼
                  ┌──────────────┐
                  │   Message    │ (new)
                  │  id: UUID    │
                  │  conv_id     │
                  └──────────────┘
```

---

## Existing Entities (Phase II)

### User

**Location**: `backend/src/models/user.py` (existing)

```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """User entity from Phase II - DO NOT MODIFY."""
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    email: str = Field(unique=True, nullable=False, index=True)
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task

**Location**: `backend/src/models/task.py` (existing)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Task(SQLModel, table=True):
    """Task entity from Phase II - DO NOT MODIFY."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(nullable=False, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)
    is_completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

---

## New Entities (Phase III)

### Conversation

**Location**: `backend/src/models/conversation.py` (new)

**Purpose**: Represents a chat session between a user and the AI assistant.

**SQLModel Definition**:

```python
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

    # Relationships (for SQLModel queries, not stored in DB)
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Indexes**:
- `user_id` (for retrieving user's conversations)
- `created_at` (for chronological ordering)
- `updated_at` (for "recent conversations" queries)

**Constraints**:
- `user_id` must reference existing user (foreign key constraint)
- Cascade delete: When user deleted, all conversations deleted

**Business Rules**:
- Title auto-generated from first user message (truncated to 50 chars)
- `updated_at` updated whenever new message added
- Conversations older than 30 days may be archived (future enhancement)

---

### Message

**Location**: `backend/src/models/message.py` (new)

**Purpose**: Represents a single message within a conversation (user or assistant).

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

class MessageRole(str, Enum):
    """Message sender role."""
    USER = "user"
    ASSISTANT = "assistant"

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

    # Relationships (for SQLModel queries, not stored in DB)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

**Indexes**:
- `conversation_id` (for retrieving conversation messages)
- `created_at` (for chronological ordering within conversation)

**Constraints**:
- `conversation_id` must reference existing conversation (foreign key constraint)
- `role` must be either 'user' or 'assistant' (enum constraint)
- Cascade delete: When conversation deleted, all messages deleted

**Business Rules**:
- Messages are immutable (no updates after creation)
- Messages ordered by `created_at` within conversation
- User messages always followed by assistant response (enforced in application logic)

---

## Database Migration

### Migration Script (Alembic)

**File**: `backend/alembic/versions/003_add_conversations_messages.py`

```python
"""Add conversations and messages tables for Phase III

Revision ID: 003
Revises: 002
Create Date: 2026-01-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create indexes for conversations
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
    )

    # Create indexes for messages
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    # Drop messages table and indexes
    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    # Drop conversations table and indexes
    op.drop_index('idx_conversations_updated_at', table_name='conversations')
    op.drop_index('idx_conversations_created_at', table_name='conversations')
    op.drop_index('idx_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
```

### Migration Commands

```bash
# Generate migration (if using auto-generation)
cd backend
alembic revision --autogenerate -m "Add conversations and messages tables"

# Apply migration
alembic upgrade head

# Verify migration
alembic current
```

---

## Query Patterns

### Common Queries

**1. Get User's Recent Conversations**

```python
from sqlmodel import select

conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
    .limit(20)
).all()
```

**2. Get Conversation Messages (Paginated)**

```python
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.asc())
    .offset(offset)
    .limit(50)
).all()
```

**3. Create New Conversation with First Message**

```python
# Create conversation
conversation = Conversation(
    user_id=user_id,
    title=None  # Will be set after first message
)
session.add(conversation)
session.flush()  # Get conversation.id

# Add first user message
user_message = Message(
    conversation_id=conversation.id,
    role=MessageRole.USER,
    content=user_input
)
session.add(user_message)

# Generate title from first message
conversation.title = user_input[:50] + ("..." if len(user_input) > 50 else "")

session.commit()
```

**4. Add Message to Existing Conversation**

```python
# Add message
message = Message(
    conversation_id=conversation_id,
    role=role,
    content=content
)
session.add(message)

# Update conversation timestamp
conversation = session.get(Conversation, conversation_id)
conversation.updated_at = datetime.utcnow()

session.commit()
```

**5. Get Conversation with Messages (Eager Loading)**

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload

conversation = session.exec(
    select(Conversation)
    .where(Conversation.id == conversation_id)
    .where(Conversation.user_id == user_id)  # User ownership check
    .options(selectinload(Conversation.messages))
).first()

if conversation:
    messages = conversation.messages  # Already loaded
```

---

## Data Validation Rules

### Conversation

- `user_id`: Must reference existing user
- `title`: Max 200 characters, nullable
- `created_at`, `updated_at`: Auto-managed, not user-provided

### Message

- `conversation_id`: Must reference existing conversation owned by user
- `role`: Must be 'user' or 'assistant'
- `content`: Required, no max length (TEXT field)
- `created_at`: Auto-managed, not user-provided

---

## Performance Considerations

### Indexes

All critical query paths are indexed:
- User's conversations: `conversations.user_id`
- Recent conversations: `conversations.updated_at`
- Conversation messages: `messages.conversation_id`
- Message ordering: `messages.created_at`

### Query Optimization

- Pagination for message lists (50 messages per page)
- Limit conversation list to 20 most recent
- Eager loading for conversation + messages when needed
- Avoid N+1 queries with selectinload

### Storage Estimates

- Conversation: ~100 bytes per record
- Message: ~500 bytes average per message (varies with content length)
- 1000 users × 10 conversations × 50 messages = 250MB (manageable)

---

## Security Considerations

### User Ownership Enforcement

All queries MUST filter by user_id:

```python
# ✅ CORRECT - Enforces user ownership
conversation = session.exec(
    select(Conversation)
    .where(Conversation.id == conversation_id)
    .where(Conversation.user_id == user_id_from_jwt)  # Critical!
).first()

# ❌ WRONG - Missing user ownership check
conversation = session.get(Conversation, conversation_id)  # Vulnerable!
```

### Cascade Deletes

- User deleted → All conversations deleted → All messages deleted
- Conversation deleted → All messages deleted
- Ensures no orphaned data

---

## Testing Checklist

- [ ] Migration runs successfully on Neon PostgreSQL
- [ ] Foreign key constraints enforced
- [ ] Cascade deletes work correctly
- [ ] Indexes created and used by queries (EXPLAIN ANALYZE)
- [ ] User ownership checks prevent cross-user access
- [ ] Pagination works for large conversation histories
- [ ] Enum constraint on message.role enforced
- [ ] Timestamps auto-populate correctly

---

## Next Steps

1. Create migration script in `backend/alembic/versions/`
2. Test migration on development database
3. Update `backend/src/models/__init__.py` to export new models
4. Create Pydantic schemas for API requests/responses
5. Implement repository/service layer for conversation operations
