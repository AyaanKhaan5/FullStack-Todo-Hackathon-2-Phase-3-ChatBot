"""Authentication endpoints for signup and login."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database import get_session
from src.models.user import User
from src.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from src.utils.password import hash_password, verify_password
from src.utils.jwt import create_access_token

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user with email and password.

    Returns JWT token on successful registration.
    """
    # Check if user already exists
    statement = select(User).where(User.email == signup_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    # Create new user with hashed password
    hashed_pwd = hash_password(signup_data.password)
    new_user = User(
        name=signup_data.name,
        email=signup_data.email,
        hashed_password=hashed_pwd
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    access_token = create_access_token(
        user_id=new_user.id,
        email=new_user.email
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(new_user.id),
        email=new_user.email,
        name=new_user.name
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user with email/username and password.

    Returns JWT token on successful authentication.
    """
    # Find user by email
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate JWT token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        email=user.email,
        name=user.name
    )
