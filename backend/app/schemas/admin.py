"""
Admin schemas matching Java admin DTOs.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.user import Role


# --- Request Schemas ---

class CreateCompanyRequest(BaseModel):
    """Matches Java CreateCompanyRequest.java"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    website: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=150)


class UpdateUserStatusRequest(BaseModel):
    """Matches Java UpdateUserStatusRequest.java"""
    enabled: bool


# --- Response Schemas ---

class UserSummaryResponse(BaseModel):
    """Matches Java UserSummaryResponse.java"""
    id: int
    name: str
    email: str
    role: Role
    enabled: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}


class PlatformStatsResponse(BaseModel):
    """Matches Java PlatformStatsResponse.java"""
    total_users: int
    total_candidates: int
    total_recruiters: int
    total_admins: int
    total_companies: int


class CompanyResponse(BaseModel):
    """Matches Java CompanyResponse.java"""
    id: int
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}


class PageResponse(BaseModel):
    """
    Generic paginated response matching Spring Data Page<T>.
    Used for admin user and company listings.
    """
    content: list
    page: int
    size: int
    total_elements: int
    total_pages: int
    
    @staticmethod
    def create(content: list, page: int, size: int, total: int):
        """Create a page response from query results."""
        total_pages = (total + size - 1) // size if size > 0 else 0
        return PageResponse(
            content=content,
            page=page,
            size=size,
            total_elements=total,
            total_pages=total_pages
        )
