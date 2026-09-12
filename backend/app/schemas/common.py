"""
Common schemas matching Java common DTOs.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Matches Java ErrorResponse.java.
    Consistent error shape for all API errors.
    """
    status: int
    error: str
    message: str
    path: str
    timestamp: datetime = datetime.utcnow()
    details: Optional[list[str]] = None
    
    model_config = {"from_attributes": True}
