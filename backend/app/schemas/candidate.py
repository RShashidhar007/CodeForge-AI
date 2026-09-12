"""
Candidate profile schemas matching Java candidate DTOs.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class CandidateProfileUpdateRequest(BaseModel):
    """
    Matches Java CandidateProfileUpdateRequest.java.
    All fields optional for PUT/PATCH updates.
    """
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=150)
    bio: Optional[str] = Field(None, max_length=2000)
    skills: Optional[list[str]] = None
    github_url: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=255)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and v.strip():
            # Phone validation matching Java pattern
            pattern = r'^[+0-9()\-\s]{6,20}$'
            if not re.match(pattern, v):
                raise ValueError('Phone number format is invalid')
            return v.strip()
        return None
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is not None:
            # Filter out empty strings and limit length
            return [s.strip() for s in v if s and s.strip() and len(s.strip()) <= 100][:50]
        return None


class CandidateProfileResponse(BaseModel):
    """Matches Java CandidateProfileResponse.java"""
    user_id: int
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: list[str] = []
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    model_config = {"from_attributes": True}
