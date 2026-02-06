"""Task service for business logic."""
from sqlmodel import Session, select
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
from typing import List, Optional
import uuid


class TaskService:
    """Service for task operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def create_task(self, user_id: uuid.UUID, task_data: TaskCreate) -> Task:
        """Create a new task for the user."""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            is_completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_tasks(self, user_id: uuid.UUID) -> List[Task]:
        """Get all tasks for the user."""
        statement = select(Task).where(Task.user_id == user_id)
        tasks = self.session.exec(statement).all()
        return list(tasks)

    def get_task(self, user_id: uuid.UUID, task_id: int) -> Optional[Task]:
        """Get a specific task for the user."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        return self.session.exec(statement).first()

    def update_task(
        self,
        user_id: uuid.UUID,
        task_id: int,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Update a task for the user."""
        task = self.get_task(user_id, task_id)
        if not task:
            return None

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.is_completed is not None:
            task.is_completed = task_data.is_completed

        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, user_id: uuid.UUID, task_id: int) -> bool:
        """Delete a task for the user."""
        task = self.get_task(user_id, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_complete(self, user_id: uuid.UUID, task_id: int) -> Optional[Task]:
        """Toggle task completion status."""
        task = self.get_task(user_id, task_id)
        if not task:
            return None

        task.is_completed = not task.is_completed
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
