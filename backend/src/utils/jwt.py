"""JWT token utilities."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from src.config import settings
import uuid


def create_access_token(user_id: uuid.UUID, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User's UUID
        email: User's email address
        expires_delta: Optional custom expiration time (default: 7 days)

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default: 7 days
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode = {
        "sub": str(user_id),  # Subject (user_id)
        "email": email,
        "exp": expire
    }

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError as e:
        raise e
