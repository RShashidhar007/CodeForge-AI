"""
Security utilities: password hashing and JWT token generation/validation.
Matches Java JwtService.java and Spring Security BCryptPasswordEncoder.
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# BCrypt context for password hashing (matching Spring Security BCryptPasswordEncoder)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using BCrypt.
    Matches Spring Security's BCryptPasswordEncoder.encode().
    BCrypt has a 72-byte limit, so we truncate if necessary.
    """
    # BCrypt has a max of 72 bytes - truncate if needed
    truncated_password = password[:72]
    return pwd_context.hash(truncated_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a BCrypt hash.
    Matches Spring Security's BCryptPasswordEncoder.matches().
    BCrypt has a 72-byte limit, so we truncate if necessary.
    """
    # BCrypt has a max of 72 bytes - truncate if needed
    truncated_password = plain_password[:72]
    return pwd_context.verify(truncated_password, hashed_password)


def create_access_token(email: str, role: str) -> str:
    """
    Generate a JWT access token for the given user.
    Matches Java JwtService.generateToken().
    
    Args:
        email: User's email (stored in JWT 'sub' claim)
        role: User's role (stored in JWT 'role' claim)
    
    Returns:
        Encoded JWT token string
    """
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(seconds=settings.jwt_expiration_seconds)
    
    payload = {
        "sub": email,  # Subject: user email
        "role": role,  # Custom claim: user role
        "iat": issued_at,  # Issued at
        "exp": expires_at  # Expiration
    }
    
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    Matches Java JwtService.extractEmail() and validation logic.
    
    Args:
        token: JWT token string
    
    Returns:
        Token payload dict if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


def extract_email_from_token(token: str) -> Optional[str]:
    """
    Extract email from JWT token.
    Matches Java JwtService.extractEmail().
    
    Args:
        token: JWT token string
    
    Returns:
        User email if token is valid, None otherwise
    """
    payload = decode_access_token(token)
    if payload:
        return payload.get("sub")
    return None


def get_expiration_seconds() -> int:
    """
    Get JWT expiration duration in seconds.
    Matches Java JwtService.getExpirationSeconds().
    """
    return settings.jwt_expiration_seconds
