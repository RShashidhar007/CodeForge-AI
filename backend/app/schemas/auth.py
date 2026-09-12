"""
Authentication schemas matching Java auth DTOs.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import Role


# --- Request Schemas ---

class RegisterCandidateRequest(BaseModel):
    """Matches Java RegisterCandidateRequest.java"""
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @field_validator('name')
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Name is required')
        return v.strip()


class RegisterRecruiterRequest(BaseModel):
    """Matches Java RegisterRecruiterRequest.java"""
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    designation: Optional[str] = Field(None, max_length=150)
    company_name: Optional[str] = Field(None, max_length=200)
    
    @field_validator('name')
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Name is required')
        return v.strip()


class LoginRequest(BaseModel):
    """Matches Java LoginRequest.java"""
    email: EmailStr
    password: str = Field(..., min_length=1)


# --- Response Schemas ---

class UserResponse(BaseModel):
    """
    Matches Java UserResponse.java.
    This is what gets returned from any API that exposes user info.
    """
    id: int
    name: str
    email: str
    role: Role
    enabled: bool
    
    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    """Matches Java LoginResponse.java"""
    token: str
    token_type: str = "Bearer"
    expires_in_seconds: int
    user: UserResponse
    
    model_config = {"from_attributes": True}
