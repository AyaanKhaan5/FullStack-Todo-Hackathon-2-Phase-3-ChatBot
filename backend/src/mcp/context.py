"""JWT context extraction for MCP tools."""
from fastapi import Depends
from ..api.dependencies import get_current_user


async def extract_user_context(
    user_id: str = Depends(get_current_user)
) -> dict:
    """
    Extract user context from JWT for MCP tools.

    This ensures user identity is derived ONLY from JWT tokens,
    never from request body or URL parameters.

    Args:
        user_id: User ID from JWT token (via dependency)

    Returns:
        Dictionary with user_id
    """
    return {
        "user_id": user_id
    }
