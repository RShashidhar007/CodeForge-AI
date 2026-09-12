"""
FastAPI dependencies for authentication and authorization.
Matches Java Spring Security filter chain and @PreAuthorize annotations.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, Role
from app.repositories.user_repository import UserRepository

# HTTP Bearer token scheme (extracts "Authorization: Bearer <token>")
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate JWT token, then load the authenticated user.
    Matches Java JwtAuthenticationFilter and SecurityContext.
    
    Raises:
        HTTPException: 401 if token is invalid or user not found/disabled
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    email: Optional[str] = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user_repo = UserRepository(db)
    user = user_repo.find_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.enabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account has been disabled"
        )
    
    return user


def require_role(required_role: Role):
    """
    Dependency factory for role-based access control.
    Matches Java @PreAuthorize("hasRole('...')") annotations.
    
    Usage:
        @router.get("/admin/stats")
        def get_stats(current_user: User = Depends(require_role(Role.ADMIN))):
            ...
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return role_checker


# Convenience dependencies for each role
get_current_candidate = require_role(Role.CANDIDATE)
get_current_recruiter = require_role(Role.RECRUITER)
get_current_admin = require_role(Role.ADMIN)
