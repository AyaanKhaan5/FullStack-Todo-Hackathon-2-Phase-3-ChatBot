"""Task management API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid

from ...database import get_session
from ...models.task import Task
from ...schemas.task import TaskCreate, TaskUpdate, TaskComplete, TaskResponse
from ..dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks for authenticated user.

    Returns tasks in descending order by creation date (newest first).
    """
    # Validate user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden - user_id does not match authenticated user"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    # Query tasks with user_id filter
    statement = select(Task).where(Task.user_id == user_uuid).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()

    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for authenticated user.

    The task is automatically associated with the user's account.
    """
    # Validate user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden - user_id does not match authenticated user"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    # Create new task
    task = Task(
        user_id=user_uuid,
        title=task_data.title,
        description=task_data.description,
        is_completed=False
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Returns 404 if task doesn't exist or doesn't belong to authenticated user.
    """
    # Validate user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden - user_id does not match authenticated user"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    # Query task with ownership check
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task (title and/or description).

    Only the authenticated user who owns the task can update it.
    """
    # Validate user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden - user_id does not match authenticated user"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    # Query task with ownership check
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    Only the authenticated user who owns the task can delete it.
    """
    # Validate user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden - user_id does not match authenticated user"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    # Query task with ownership check
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return None


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    completion_data: TaskComplete,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    Only the authenticated user who owns the task can update its status.
    """
    # Validate user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden - user_id does not match authenticated user"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    # Query task with ownership check
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    task.is_completed = completion_data.is_completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# Import datetime for updated_at
from datetime import datetime
