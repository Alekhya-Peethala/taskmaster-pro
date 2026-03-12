"""
TaskMaster Pro - Database Connection Module
Generated with GitHub Copilot assistance
Provides SQLAlchemy engine and session management for MySQL database
Constitution Principle I: Azure-Native Architecture (Azure MySQL Flexible Server)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
# Format: mysql+mysqlconnector://user:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:rootpass@localhost:3306/taskmaster"
)

# Base class for SQLAlchemy models (created early so models can import it)
Base = declarative_base()

# Check if we're in test mode (skip engine creation during test imports)
_IS_TEST = os.getenv("ENV") == "test" or "pytest" in os.getenv("_", "")

# Global engine and session factory (created lazily)
_engine = None
_SessionLocal = None

def get_engine():
    """Get or create the SQLAlchemy engine."""
    global _engine
    if _engine is None and not _IS_TEST:
        # Create SQLAlchemy engine with connection pooling
        # Pool settings optimized for Azure MySQL Flexible Server
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,          # Verify connections before using
            pool_size=10,                 # Connection pool size
            max_overflow=20,              # Additional connections when pool is full
            pool_recycle=3600,            # Recycle connections after 1 hour
            echo=False,                   # Set to True for SQL query logging (development)
        )
    return _engine

def get_session_local():
    """Get or create the SessionLocal factory."""
    global _SessionLocal
    if _SessionLocal is None and not _IS_TEST:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    return _SessionLocal

# For backwards compatibility, expose engine and SessionLocal as module attributes
# These will be None in test mode and created lazily in production
engine = get_engine() if not _IS_TEST else None
SessionLocal = get_session_local() if not _IS_TEST else None


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to provide database sessions to FastAPI endpoints.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage:
        @app.get("/api/tasks")
        def get_tasks(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables defined in models.
    Should be called on application startup.
    
    For production, use Alembic migrations instead of this function.
    """
    # Import all models here to ensure they are registered with Base
    # from .models.task import Task  # Uncomment when Task model is created
    
    Base.metadata.create_all(bind=engine)
