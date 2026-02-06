"""JWT authentication middleware."""
from jose import JWTError, jwt
from fastapi import HTTPException, status
from ..config import settings


def verify_jwt_token(token: str) -> str:
    """
    Verify JWT token and extract user_id.

    Args:
        token: JWT token string

    Returns:
        str: User ID from token's 'sub' claim

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        return user_id
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired JWT token: {str(e)}"
        )
