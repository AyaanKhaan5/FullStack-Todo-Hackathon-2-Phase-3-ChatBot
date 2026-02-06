"""Database connection and session management."""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from .config import settings

# Create SQLModel engine with Neon PostgreSQL connection
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Max connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use (handles serverless)
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create all database tables (for development/testing only)."""
    SQLModel.metadata.create_all(engine)
