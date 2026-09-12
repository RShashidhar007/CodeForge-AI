"""
Admin bootstrap logic matching Java AdminInitializer.
Creates initial admin account on startup if configured.
"""
import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, Role
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


def bootstrap_admin(db: Session):
    """
    Creates the platform's first ADMIN account on startup, if one doesn't
    already exist. Matches Java AdminInitializer.run().
    
    The admin's email/password come from environment variables, not public registration.
    """
    if not settings.admin_email or not settings.admin_password:
        logger.warning(
            "ADMIN_EMAIL / ADMIN_PASSWORD not set -- skipping admin bootstrap. "
            "No admin account will exist until these are configured."
        )
        return
    
    user_repo = UserRepository(db)
    
    if user_repo.exists_by_email(settings.admin_email):
        logger.info(f"Admin account already exists for {settings.admin_email}, skipping bootstrap.")
        return
    
    admin = User(
        name=settings.admin_name,
        email=settings.admin_email,
        password_hash=hash_password(settings.admin_password),
        role=Role.ADMIN,
        enabled=True
    )
    
    user_repo.save(admin)
    db.commit()
    
    logger.info(f"Bootstrapped initial admin account: {settings.admin_email}")
