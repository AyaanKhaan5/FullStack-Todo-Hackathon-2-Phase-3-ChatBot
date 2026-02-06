"""Authentication request and response schemas."""
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user signup."""
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=100, description="User's password (min 8 characters)")


class LoginRequest(BaseModel):
    """Request schema for user login."""
    email: str = Field(..., description="User's email or username")
    password: str = Field(..., description="User's password")


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User name")
