"""API dependencies for dependency injection."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..middleware.auth import verify_jwt_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        str: User ID extracted from JWT token

    Raises:
        HTTPException: If token is missing or invalid
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    return verify_jwt_token(credentials.credentials)
