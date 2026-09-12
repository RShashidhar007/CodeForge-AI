"""
Authentication service matching Java AuthService.java.
Handles registration and login for all user roles.
"""
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token, get_expiration_seconds
from app.exceptions.custom_exceptions import DuplicateResourceException, ResourceNotFoundException, BadCredentialsException, DisabledException
from app.models.user import User, Role
from app.models.candidate import Candidate
from app.models.recruiter import Recruiter
from app.repositories.user_repository import UserRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.recruiter_repository import RecruiterRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.auth import (
    RegisterCandidateRequest,
    RegisterRecruiterRequest,
    LoginRequest,
    LoginResponse,
    UserResponse
)


class AuthService:
    """
    Handles the three public entry points into the system: candidate
    registration, recruiter registration, and login.
    Matches Java AuthService.java.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.candidate_repo = CandidateRepository(db)
        self.recruiter_repo = RecruiterRepository(db)
        self.company_repo = CompanyRepository(db)
    
    def register_candidate(self, request: RegisterCandidateRequest) -> UserResponse:
        """
        Register a new candidate user.
        Matches Java: @Transactional public UserResponse registerCandidate(...)
        """
        email = request.email.lower().strip()
        
        if self.user_repo.exists_by_email(email):
            raise DuplicateResourceException("An account with this email already exists.")
        
        # Create user
        user = User(
            name=request.name.strip(),
            email=email,
            password_hash=hash_password(request.password),
            role=Role.CANDIDATE,
            enabled=True
        )
        user = self.user_repo.save(user)
        
        # Create candidate profile
        candidate = Candidate(id=user.id)
        self.db.add(candidate)
        self.db.commit()
        
        return self._user_to_response(user)
    
    def register_recruiter(self, request: RegisterRecruiterRequest) -> UserResponse:
        """
        Register a new recruiter user.
        Matches Java: @Transactional public UserResponse registerRecruiter(...)
        """
        email = request.email.lower().strip()
        
        if self.user_repo.exists_by_email(email):
            raise DuplicateResourceException("An account with this email already exists.")
        
        # Find company if specified
        company = None
        if request.company_name and request.company_name.strip():
            company = self.company_repo.find_by_name_ignore_case(request.company_name.strip())
            if not company:
                raise ResourceNotFoundException(
                    f"No company found named '{request.company_name}'. "
                    "Ask an admin to create it first, or register without a company for now."
                )
        
        # Create user
        user = User(
            name=request.name.strip(),
            email=email,
            password_hash=hash_password(request.password),
            role=Role.RECRUITER,
            enabled=True
        )
        user = self.user_repo.save(user)
        
        # Create recruiter profile
        recruiter = Recruiter(
            id=user.id,
            designation=request.designation,
            company_id=company.id if company else None
        )
        self.db.add(recruiter)
        self.db.commit()
        
        return self._user_to_response(user)
    
    def login(self, request: LoginRequest) -> LoginResponse:
        """
        Authenticate user and generate JWT token.
        Matches Java: public LoginResponse login(LoginRequest request)
        """
        email = request.email.lower().strip()
        
        user = self.user_repo.find_by_email(email)
        if not user:
            raise BadCredentialsException("Invalid email or password")
        
        if not verify_password(request.password, user.password_hash):
            raise BadCredentialsException("Invalid email or password")
        
        if not user.enabled:
            raise DisabledException("This account has been disabled")
        
        # Generate JWT token
        token = create_access_token(user.email, user.role.value)
        
        return LoginResponse(
            token=token,
            token_type="Bearer",
            expires_in_seconds=get_expiration_seconds(),
            user=self._user_to_response(user)
        )
    
    def _user_to_response(self, user: User) -> UserResponse:
        """Convert User entity to UserResponse DTO."""
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            enabled=user.enabled
        )
