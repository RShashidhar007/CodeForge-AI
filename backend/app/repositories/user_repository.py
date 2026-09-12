"""
User repository matching Java UserRepository interface.
"""
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User, Role


class UserRepository:
    """Data access layer for User entity matching Java UserRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Matches Java: Optional<User> findByEmail(String email)"""
        return self.db.query(User).filter(User.email == email).first()
    
    def exists_by_email(self, email: str) -> bool:
        """Matches Java: boolean existsByEmail(String email)"""
        return self.db.query(
            self.db.query(User).filter(User.email == email).exists()
        ).scalar()
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def save(self, user: User) -> User:
        """Save or update a user."""
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
    
    def find_by_role(self, role: Role, page: int, size: int) -> tuple[list[User], int]:
        """
        Matches Java: Page<User> findByRole(Role role, Pageable pageable)
        Returns (users, total_count)
        """
        query = self.db.query(User).filter(User.role == role)
        total = query.count()
        users = query.offset(page * size).limit(size).all()
        return users, total
    
    def find_all(self, page: int, size: int) -> tuple[list[User], int]:
        """
        Find all users with pagination.
        Returns (users, total_count)
        """
        query = self.db.query(User)
        total = query.count()
        users = query.offset(page * size).limit(size).all()
        return users, total
    
    def count_by_role(self, role: Role) -> int:
        """Matches Java: long countByRole(Role role)"""
        return self.db.query(User).filter(User.role == role).count()
    
    def count_all(self) -> int:
        """Count all users."""
        return self.db.query(User).count()
