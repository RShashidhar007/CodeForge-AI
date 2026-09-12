"""
Database session dependency for FastAPI dependency injection.
"""
from typing import Generator
from sqlalchemy.orm import Session

from app.db.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Automatically closes the session after the request is complete.
    
    Usage in FastAPI endpoints:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            # Use db here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
