"""
Company repository matching Java CompanyRepository interface.
"""
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:
    """Data access layer for Company entity matching Java CompanyRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_name_ignore_case(self, name: str) -> Optional[Company]:
        """Matches Java: Optional<Company> findByNameIgnoreCase(String name)"""
        return (
            self.db.query(Company)
            .filter(func.lower(Company.name) == name.lower())
            .first()
        )
    
    def exists_by_name_ignore_case(self, name: str) -> bool:
        """Matches Java: boolean existsByNameIgnoreCase(String name)"""
        return self.db.query(
            self.db.query(Company)
            .filter(func.lower(Company.name) == name.lower())
            .exists()
        ).scalar()
    
    def save(self, company: Company) -> Company:
        """Save or update a company."""
        self.db.add(company)
        self.db.flush()
        self.db.refresh(company)
        return company
    
    def find_all(self, page: int, size: int) -> tuple[list[Company], int]:
        """
        Find all companies with pagination.
        Returns (companies, total_count)
        """
        query = self.db.query(Company)
        total = query.count()
        companies = query.offset(page * size).limit(size).all()
        return companies, total
    
    def count_all(self) -> int:
        """Count all companies."""
        return self.db.query(Company).count()
