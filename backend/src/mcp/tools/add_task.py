"""MCP tool for adding tasks."""
from typing import Optional
from ...utils.date_parser import parse_due_date


def create_add_task_tool(task_service, user_uuid):
    """
    Create add_task MCP tool with user context.

    Args:
        task_service: TaskService instance
        user_uuid: User UUID from JWT

    Returns:
        add_task function
    """
    def add_task(
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> dict:
        """
        Create a new task for the user.

        Args:
            title: Task title (required, 1-500 characters)
            description: Task description (optional, max 5000 characters)
            due_date: Due date in ISO 8601 or natural language (optional)

        Returns:
            Created task as dictionary

        Raises:
            ValueError: If title is invalid or due_date format is invalid
        """
        # Validate title
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        if len(title) > 500:
            raise ValueError("Task title cannot exceed 500 characters")

        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = parse_due_date(due_date)
            except ValueError as e:
                raise ValueError(f"Invalid due date: {str(e)}")

        # Create task using TaskService
        from ...schemas.task import TaskCreate

        task_data = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None
        )

        task = task_service.create_task(user_uuid, task_data)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            "created_at": task.created_at.isoformat(),
            "due_date": parsed_due_date.isoformat() if parsed_due_date else None
        }

    return add_task
