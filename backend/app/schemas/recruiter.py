"""
Recruiter profile schemas matching Java recruiter DTOs.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class RecruiterProfileUpdateRequest(BaseModel):
    """Matches Java RecruiterProfileUpdateRequest.java"""
    phone: Optional[str] = Field(None, max_length=20)
    designation: Optional[str] = Field(None, max_length=150)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and v.strip():
            pattern = r'^[+0-9()\-\s]{6,20}$'
            if not re.match(pattern, v):
                raise ValueError('Phone number format is invalid')
            return v.strip()
        return None


class RecruiterProfileResponse(BaseModel):
    """Matches Java RecruiterProfileResponse.java"""
    user_id: int
    name: str
    email: str
    phone: Optional[str] = None
    designation: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    
    model_config = {"from_attributes": True}
