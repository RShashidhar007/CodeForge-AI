"""
Admin routes matching Java AdminController.
All endpoints require ADMIN role authentication.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User, Role
from app.schemas.admin import (
    UserSummaryResponse,
    PlatformStatsResponse,
    CompanyResponse,
    CreateCompanyRequest,
    UpdateUserStatusRequest,
    PageResponse
)
from app.services.admin_service import AdminService

router = APIRouter()


@router.get("/users", response_model=PageResponse)
def list_users(
    role: Optional[Role] = Query(None),
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List users with optional role filter and pagination.
    Matches Java: GET /api/admin/users
    """
    service = AdminService(db)
    return service.list_users(role, page, size)


@router.patch("/users/{id}/status", response_model=UserSummaryResponse)
def set_user_enabled(
    id: int,
    request: UpdateUserStatusRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Enable or disable a user account.
    Matches Java: PATCH /api/admin/users/{id}/status
    """
    service = AdminService(db)
    return service.set_user_enabled(id, request.enabled)


@router.get("/stats", response_model=PlatformStatsResponse)
def get_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get platform statistics.
    Matches Java: GET /api/admin/stats
    """
    service = AdminService(db)
    return service.get_stats()


@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    request: CreateCompanyRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new company.
    Matches Java: POST /api/admin/companies
    """
    service = AdminService(db)
    return service.create_company(request)


@router.get("/companies", response_model=PageResponse)
def list_companies(
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List all companies with pagination.
    Matches Java: GET /api/admin/companies
    """
    service = AdminService(db)
    return service.list_companies(page, size)
