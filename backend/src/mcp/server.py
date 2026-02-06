"""MCP server for stateless tool functions."""
from typing import Callable, List
from sqlmodel import Session
from ..services.task_service import TaskService
import uuid


class TaskMCPServer:
    """MCP server that creates stateless tool functions with user context."""

    def __init__(self, session_factory: Callable[[], Session]):
        """
        Initialize MCP server.

        Args:
            session_factory: Factory function that creates database sessions
        """
        self.session_factory = session_factory

    def create_tool_functions(self, user_id: str) -> List[Callable]:
        """
        Create stateless tool functions with user context.

        All tools are stateless - they receive user_id via closure and
        create fresh database sessions per invocation.

        Args:
            user_id: User ID from JWT token

        Returns:
            List of tool functions for the AI agent
        """
        user_uuid = uuid.UUID(user_id)

        def add_task(
            title: str,
            description: str = None,
            due_date: str = None
        ) -> dict:
            """
            Create a new task for the user.

            Args:
                title: Task title (required)
                description: Task description (optional)
                due_date: Due date in ISO 8601 or natural language (optional)

            Returns:
                Created task as dictionary
            """
            with self.session_factory() as session:
                task_service = TaskService(session)
                from ..schemas.task import TaskCreate

                task_data = TaskCreate(
                    title=title,
                    description=description
                )

                task = task_service.create_task(user_uuid, task_data)

                return {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat()
                }

        # Return list of tool functions
        # Note: Only add_task for now, other tools will be added in Phase 4
        return [add_task]
