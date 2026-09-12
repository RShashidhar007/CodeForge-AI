"""
SQLAlchemy ORM models for Month 3 agent system.
Stores AI tasks, execution history, patches, and approvals.
"""
from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class AITask(Base):
    """
    Represents an AI task created by a user.
    Stores the task definition and tracks its lifecycle.
    """
    __tablename__ = "ai_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Task definition
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(String(50), nullable=False, index=True)  # CODE_EXPLANATION, BUG_FIX, etc.
    
    # Lifecycle
    status = Column(String(50), nullable=False, default="QUEUED", index=True)  # QUEUED, PLANNING, ANALYZING, etc.
    current_agent = Column(String(100), nullable=True)  # Currently executing agent
    progress_percent = Column(Integer, default=0)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="ai_tasks")
    project = relationship("Project", back_populates="ai_tasks_month3")
    executions = relationship("AgentExecution", back_populates="task", cascade="all, delete-orphan")
    patches = relationship("TaskPatch", back_populates="task", cascade="all, delete-orphan")
    approvals = relationship("TaskApproval", back_populates="task", cascade="all, delete-orphan")
    test_results = relationship("TaskTestResult", back_populates="task", cascade="all, delete-orphan")
    workspaces = relationship("TaskWorkspace", back_populates="task", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_ai_tasks_user_id', 'user_id'),
        Index('idx_ai_tasks_project_id', 'project_id'),
        Index('idx_ai_tasks_status', 'status'),
        Index('idx_ai_tasks_task_type', 'task_type'),
        Index('idx_ai_tasks_created_at', 'created_at'),
    )


class AgentExecution(Base):
    """
    Records execution history of each agent for a task.
    Provides audit trail and debugging information.
    """
    __tablename__ = "agent_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('ai_tasks.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Agent info
    agent_name = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)  # RUNNING, SUCCESS, FAILED, SKIPPED
    
    # Execution details
    input_summary = Column(Text, nullable=True)
    output_summary = Column(Text, nullable=True)
    tool_calls = Column(Integer, default=0)
    tokens_used = Column(Integer, nullable=True)
    
    # Timing
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    
    # Relationships
    task = relationship("AITask", back_populates="executions")
    
    # Indexes
    __table_args__ = (
        Index('idx_agent_executions_task_id', 'task_id'),
        Index('idx_agent_executions_agent_name', 'agent_name'),
        Index('idx_agent_executions_status', 'status'),
    )


class TaskPatch(Base):
    """
    Represents a proposed code patch from the Coding agent.
    Stores patch content and validation/review status.
    """
    __tablename__ = "task_patches"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('ai_tasks.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Source
    agent_id = Column(String(100), nullable=True)  # Which agent generated this
    
    # Content
    target_files = Column(Text, nullable=False)  # JSON array of filenames
    patch_content = Column(Text, nullable=False)  # Unified diff format
    
    # Status
    validation_status = Column(String(50), nullable=False, default="PENDING", index=True)  # PENDING, VALID, INVALID, APPLIED
    review_status = Column(String(50), nullable=True, index=True)  # PENDING, APPROVED, REJECTED, CHANGES_REQUESTED
    review_comments = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    applied_at = Column(DateTime, nullable=True)
    
    # Relationships
    task = relationship("AITask", back_populates="patches")
    
    # Indexes
    __table_args__ = (
        Index('idx_task_patches_task_id', 'task_id'),
        Index('idx_task_patches_validation_status', 'validation_status'),
        Index('idx_task_patches_review_status', 'review_status'),
    )
    
    def get_target_files_list(self) -> list:
        """Parse JSON target files."""
        try:
            return json.loads(self.target_files)
        except:
            return []
    
    def set_target_files_list(self, files: list):
        """Set target files from list."""
        self.target_files = json.dumps(files)


class TaskApproval(Base):
    """
    Records user approval decisions for tasks.
    Audit trail for human approval workflow.
    """
    __tablename__ = "task_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('ai_tasks.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Decision
    action = Column(String(50), nullable=False)  # APPROVED, REJECTED, REQUESTED_CHANGES
    comment = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    task = relationship("AITask", back_populates="approvals")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_task_approvals_task_id', 'task_id'),
        Index('idx_task_approvals_user_id', 'user_id'),
    )


class TaskTestResult(Base):
    """
    Records test execution results for a task.
    Allows tracking of multiple test runs and failures.
    """
    __tablename__ = "task_test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('ai_tasks.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Execution info
    execution_number = Column(Integer, nullable=False, index=True)
    test_command = Column(String(255), nullable=False)
    
    # Results
    exit_code = Column(Integer, nullable=False)
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Summary
    passed_count = Column(Integer, nullable=True)
    failed_count = Column(Integer, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    task = relationship("AITask", back_populates="test_results")
    
    # Indexes
    __table_args__ = (
        Index('idx_task_test_results_task_id', 'task_id'),
        Index('idx_task_test_results_execution_number', 'execution_number'),
    )


class TaskWorkspace(Base):
    """
    Tracks working spaces for task execution.
    May be Docker container, git branch, or temporary directory.
    """
    __tablename__ = "task_workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('ai_tasks.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Workspace identification
    workspace_type = Column(String(50), nullable=False)  # DOCKER_CONTAINER, GIT_BRANCH, TEMPORARY
    workspace_identifier = Column(String(255), nullable=False)  # Container ID, branch name, or path
    
    # Status
    status = Column(String(50), nullable=False, default="CREATED", index=True)  # CREATED, ACTIVE, CLEANED_UP
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    cleaned_up_at = Column(DateTime, nullable=True)
    
    # Relationships
    task = relationship("AITask", back_populates="workspaces")
    
    # Indexes
    __table_args__ = (
        Index('idx_task_workspaces_task_id', 'task_id'),
        Index('idx_task_workspaces_status', 'status'),
    )
