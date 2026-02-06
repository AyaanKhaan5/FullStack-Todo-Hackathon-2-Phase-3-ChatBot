# MCP Tools Specification

**Feature**: 003-ai-chatbot-mcp
**Date**: 2026-01-15
**Version**: 1.0.0

## Overview

This document defines the 5 stateless MCP tools that enable the AI agent to interact with the task management system. All tools are database-backed and enforce user ownership through JWT-derived user context.

---

## Tool Definitions

### 1. add_task

**Purpose**: Create a new task for the authenticated user

**Signature**:
```python
def add_task(
    title: str,
    description: str | None = None,
    due_date: str | None = None
) -> Task
```

**Parameters**:
- `title` (required): Task title (1-500 characters)
- `description` (optional): Task description (max 5000 characters)
- `due_date` (optional): Due date in ISO 8601 format (e.g., "2026-01-16T15:00:00Z") or natural language (e.g., "tomorrow", "next Friday")

**Returns**: Created Task object with all fields

**Behavior**:
1. Extract user_id from JWT context (never from parameters)
2. Parse due_date if provided (natural language → datetime)
3. Create Task record in database with user_id
4. Return created task

**Error Handling**:
- Invalid title (empty, too long): Raise ValueError
- Invalid due_date format: Raise ValueError
- Database error: Raise DatabaseError

**Example**:
```python
task = add_task(
    title="Buy groceries",
    description="Milk, eggs, bread",
    due_date="2026-01-16T15:00:00Z"
)
# Returns: Task(id=123, user_id=<from JWT>, title="Buy groceries", ...)
```

---

### 2. list_tasks

**Purpose**: Retrieve user's tasks with optional filtering

**Signature**:
```python
def list_tasks(
    filter: str | None = None,
    limit: int = 50
) -> List[Task]
```

**Parameters**:
- `filter` (optional): Filter criteria
  - `"completed"`: Only completed tasks
  - `"incomplete"`: Only incomplete tasks
  - `"overdue"`: Tasks past due date
  - `"today"`: Tasks due today
  - `"week"`: Tasks due this week
  - `None`: All tasks
- `limit` (optional): Maximum number of tasks to return (default 50, max 100)

**Returns**: List of Task objects matching filter

**Behavior**:
1. Extract user_id from JWT context
2. Query tasks table filtered by user_id
3. Apply additional filter if provided
4. Order by: incomplete first, then by due_date (nulls last), then by created_at
5. Limit results
6. Return task list

**Error Handling**:
- Invalid filter value: Raise ValueError
- Invalid limit (< 1 or > 100): Raise ValueError
- Database error: Raise DatabaseError

**Example**:
```python
tasks = list_tasks(filter="today", limit=10)
# Returns: [Task(...), Task(...), ...]
```

---

### 3. complete_task

**Purpose**: Toggle task completion status

**Signature**:
```python
def complete_task(task_id: int) -> Task
```

**Parameters**:
- `task_id` (required): Task ID to complete/uncomplete

**Returns**: Updated Task object

**Behavior**:
1. Extract user_id from JWT context
2. Query task by id AND user_id (user ownership check)
3. If task not found or not owned by user: Raise NotFoundError
4. Toggle is_completed field
5. Update updated_at timestamp
6. Commit to database
7. Return updated task

**Error Handling**:
- Task not found: Raise NotFoundError
- Task not owned by user: Raise NotFoundError (don't reveal existence)
- Database error: Raise DatabaseError

**Example**:
```python
task = complete_task(task_id=123)
# Returns: Task(id=123, is_completed=True, ...)
```

---

### 4. update_task

**Purpose**: Update task properties

**Signature**:
```python
def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    due_date: str | None = None
) -> Task
```

**Parameters**:
- `task_id` (required): Task ID to update
- `title` (optional): New title (1-500 characters)
- `description` (optional): New description (max 5000 characters, empty string to clear)
- `due_date` (optional): New due date (ISO 8601 or natural language, empty string to clear)

**Returns**: Updated Task object

**Behavior**:
1. Extract user_id from JWT context
2. Query task by id AND user_id (user ownership check)
3. If task not found or not owned by user: Raise NotFoundError
4. Update provided fields only (None = no change, "" = clear field)
5. Parse due_date if provided
6. Update updated_at timestamp
7. Commit to database
8. Return updated task

**Error Handling**:
- Task not found: Raise NotFoundError
- Task not owned by user: Raise NotFoundError
- Invalid title/description: Raise ValueError
- Invalid due_date format: Raise ValueError
- Database error: Raise DatabaseError

**Example**:
```python
task = update_task(
    task_id=123,
    title="Buy groceries and cook dinner",
    due_date="2026-01-17T18:00:00Z"
)
# Returns: Task(id=123, title="Buy groceries and cook dinner", ...)
```

---

### 5. delete_task

**Purpose**: Delete a task

**Signature**:
```python
def delete_task(task_id: int) -> bool
```

**Parameters**:
- `task_id` (required): Task ID to delete

**Returns**: True if deleted successfully

**Behavior**:
1. Extract user_id from JWT context
2. Query task by id AND user_id (user ownership check)
3. If task not found or not owned by user: Raise NotFoundError
4. Delete task from database
5. Commit transaction
6. Return True

**Error Handling**:
- Task not found: Raise NotFoundError
- Task not owned by user: Raise NotFoundError
- Database error: Raise DatabaseError

**Example**:
```python
success = delete_task(task_id=123)
# Returns: True
```

---

## Common Patterns

### User Context Extraction

All tools receive user context through closure, not parameters:

```python
class TaskMCPServer:
    def create_tool_functions(self, user_id: str):
        """Create stateless tool functions with user context."""

        def add_task(title: str, description: str = None, due_date: str = None):
            # user_id available in closure
            with self.db_session_factory() as session:
                task = Task(user_id=user_id, title=title, ...)
                session.add(task)
                session.commit()
                return task

        return [add_task, list_tasks, complete_task, update_task, delete_task]
```

### Database Session Management

Each tool invocation creates a fresh database session:

```python
def add_task(title: str, ...):
    with db_session_factory() as session:  # New session per call
        # Perform database operations
        session.commit()
    # Session closed automatically
```

### User Ownership Enforcement

All queries MUST filter by user_id:

```python
# ✅ CORRECT
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == user_id)  # Critical!
).first()

# ❌ WRONG - Missing user ownership check
task = session.get(Task, task_id)  # Vulnerable!
```

---

## Stateless Validation Checklist

- [ ] No class instance variables storing state
- [ ] No module-level global state
- [ ] Database session created per invocation
- [ ] User context from closure/parameters only
- [ ] No caching between invocations
- [ ] Tools can be called in any order
- [ ] Server restart doesn't lose state (all in DB)

---

## Natural Language Date Parsing

Tools accept natural language dates and convert to datetime:

**Supported Formats**:
- ISO 8601: `"2026-01-16T15:00:00Z"`
- Relative: `"tomorrow"`, `"next week"`, `"in 3 days"`
- Named days: `"Monday"`, `"next Friday"`
- Special: `"today"`, `"tonight"`, `"end of month"`

**Implementation**:
```python
from dateparser import parse

def parse_due_date(date_str: str) -> datetime | None:
    """Parse natural language date to datetime."""
    if not date_str:
        return None

    # Try ISO 8601 first
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        pass

    # Try natural language
    parsed = parse(date_str, settings={'PREFER_DATES_FROM': 'future'})
    if parsed:
        return parsed

    raise ValueError(f"Invalid date format: {date_str}")
```

---

## Error Response Format

Tools raise exceptions that are caught by the AI agent:

```python
class NotFoundError(Exception):
    """Task not found or not owned by user."""
    pass

class ValueError(Exception):
    """Invalid parameter value."""
    pass

class DatabaseError(Exception):
    """Database operation failed."""
    pass
```

AI agent converts exceptions to user-friendly messages:
- NotFoundError → "I couldn't find that task. Could you describe it differently?"
- ValueError → "I need more information. Could you clarify [field]?"
- DatabaseError → "I encountered an error. Please try again."

---

## Testing Strategy

### Unit Tests

Test each tool in isolation with mocked database:

```python
def test_add_task_creates_task_with_user_id():
    user_id = "test-user-123"
    tools = mcp_server.create_tool_functions(user_id)
    add_task = tools[0]

    task = add_task(title="Test task")

    assert task.user_id == user_id
    assert task.title == "Test task"
```

### Stateless Tests

Verify tools don't maintain state:

```python
def test_tools_are_stateless():
    tools1 = mcp_server.create_tool_functions("user-1")
    tools2 = mcp_server.create_tool_functions("user-2")

    task1 = tools1[0](title="User 1 task")  # add_task
    task2 = tools2[0](title="User 2 task")

    assert task1.user_id == "user-1"
    assert task2.user_id == "user-2"
```

### User Isolation Tests

Verify user ownership enforcement:

```python
def test_complete_task_enforces_user_ownership():
    user1_tools = mcp_server.create_tool_functions("user-1")
    user2_tools = mcp_server.create_tool_functions("user-2")

    # User 1 creates task
    task = user1_tools[0](title="User 1 task")

    # User 2 tries to complete it
    with pytest.raises(NotFoundError):
        user2_tools[2](task.id)  # complete_task
```

---

## Integration with OpenAI Agents SDK

Tools are registered with the AI agent:

```python
from swarm import Agent

task_agent = Agent(
    name="Task Manager",
    instructions="""
    You help users manage their todo tasks through natural language.
    Use the provided tools to create, list, update, complete, and delete tasks.
    Always confirm actions with the user before performing destructive operations.
    """,
    functions=[add_task, list_tasks, complete_task, update_task, delete_task]
)
```

Agent automatically calls appropriate tool based on user intent:
- "add a task to buy milk" → calls `add_task(title="buy milk")`
- "what are my tasks?" → calls `list_tasks()`
- "mark the grocery task as done" → calls `complete_task(task_id=...)`

---

## Next Steps

1. Implement MCP server in `backend/src/mcp/server.py`
2. Implement individual tools in `backend/src/mcp/tools/`
3. Create unit tests for each tool
4. Integrate with OpenAI Agents SDK
5. Test end-to-end with chat endpoint
