"""
Admin service matching Java AdminService.java.
Admin-only operations for user and company management.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ResourceNotFoundException, DuplicateResourceException
from app.models.user import Role
from app.models.company import Company
from app.repositories.user_repository import UserRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.admin import (
    UserSummaryResponse,
    PlatformStatsResponse,
    CompanyResponse,
    PageResponse,
    CreateCompanyRequest
)


class AdminService:
    """
    Admin-only operations. Kept intentionally small for Month 1.
    Matches Java AdminService.java.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.company_repo = CompanyRepository(db)
    
    def list_users(
        self,
        role: Optional[Role],
        page: int,
        size: int
    ) -> PageResponse:
        """
        List users with optional role filter and pagination.
        Matches Java: @Transactional(readOnly = true) public Page<UserSummaryResponse> listUsers(...)
        """
        if role:
            users, total = self.user_repo.find_by_role(role, page, size)
        else:
            users, total = self.user_repo.find_all(page, size)
        
        content = [
            UserSummaryResponse(
                id=u.id,
                name=u.name,
                email=u.email,
                role=u.role,
                enabled=u.enabled,
                created_at=u.created_at
            )
            for u in users
        ]
        
        return PageResponse.create(content, page, size, total)
    
    def get_stats(self) -> PlatformStatsResponse:
        """
        Get platform statistics.
        Matches Java: @Transactional(readOnly = true) public PlatformStatsResponse getStats()
        """
        return PlatformStatsResponse(
            total_users=self.user_repo.count_all(),
            total_candidates=self.user_repo.count_by_role(Role.CANDIDATE),
            total_recruiters=self.user_repo.count_by_role(Role.RECRUITER),
            total_admins=self.user_repo.count_by_role(Role.ADMIN),
            total_companies=self.company_repo.count_all()
        )
    
    def set_user_enabled(self, user_id: int, enabled: bool) -> UserSummaryResponse:
        """
        Enable or disable a user account.
        Matches Java: @Transactional public UserSummaryResponse setUserEnabled(...)
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found: {user_id}")
        
        user.enabled = enabled
        user = self.user_repo.save(user)
        self.db.commit()
        
        return UserSummaryResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            enabled=user.enabled,
            created_at=user.created_at
        )
    
    def create_company(self, request: CreateCompanyRequest) -> CompanyResponse:
        """
        Create a new company.
        Matches Java: @Transactional public Company createCompany(...)
        """
        name = request.name.strip()
        
        if self.company_repo.exists_by_name_ignore_case(name):
            raise DuplicateResourceException(f"A company named '{name}' already exists.")
        
        company = Company(
            name=name,
            description=request.description,
            website=request.website,
            location=request.location
        )
        company = self.company_repo.save(company)
        self.db.commit()
        
        return self._company_to_response(company)
    
    def list_companies(self, page: int, size: int) -> PageResponse:
        """
        List all companies with pagination.
        Matches Java: @Transactional(readOnly = true) public Page<Company> listCompanies(...)
        """
        companies, total = self.company_repo.find_all(page, size)
        
        content = [self._company_to_response(c) for c in companies]
        
        return PageResponse.create(content, page, size, total)
    
    def _company_to_response(self, company: Company) -> CompanyResponse:
        """Convert Company entity to CompanyResponse DTO."""
        return CompanyResponse(
            id=company.id,
            name=company.name,
            description=company.description,
            website=company.website,
            location=company.location,
            created_at=company.created_at
        )
