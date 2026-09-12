"""
SQLAlchemy models matching the Java JPA entities.
"""
from app.models.user import User, Role
from app.models.candidate import Candidate
from app.models.recruiter import Recruiter
from app.models.company import Company
from app.models.project import Project, File, GitHubToken
from app.models.ai import (
    CodeDocument,
    CodeChunk,
    AIConversation,
    AIMessage,
    AIAnalysis,
    RepositoryIndexMetadata,
    IndexStatus,
)
from app.models.agent_tasks import (
    AITask,
    AgentExecution,
    TaskPatch,
    TaskApproval,
    TaskTestResult,
    TaskWorkspace,
)

__all__ = [
    "User",
    "Role",
    "Candidate",
    "Recruiter",
    "Company",
    "Project",
    "File",
    "GitHubToken",
    "CodeDocument",
    "CodeChunk",
    "AIConversation",
    "AIMessage",
    "AIAnalysis",
    "RepositoryIndexMetadata",
    "IndexStatus",
    "AITask",
    "AgentExecution",
    "TaskPatch",
    "TaskApproval",
    "TaskTestResult",
    "TaskWorkspace",
]

