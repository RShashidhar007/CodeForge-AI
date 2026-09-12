"""
Agent task management API routes for Month 3.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.project import Project
from app.models.agent_tasks import AITask, AgentExecution, TaskApproval
from app.agents.state.models import (
    CreateTaskRequest,
    TaskResponse,
    TaskDetailResponse,
    TaskApprovalRequest,
    AgentExecutionResponse,
    TaskStatus,
    TaskType,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/projects", tags=["AI Tasks"])


@router.post("/{project_id}/ai/tasks", response_model=TaskResponse)
async def create_task(
    project_id: int,
    request: CreateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new AI task.
    
    POST /api/v1/projects/{project_id}/ai/tasks
    {
        "title": "Fix authentication bug",
        "description": "Invalid passwords are accepted",
        "task_type": "BUG_FIX",
        "selected_files": ["backend/app/services/auth_service.py"]
    }
    """
    # Verify project ownership
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create task
    task = AITask(
        user_id=current_user.id,
        project_id=project_id,
        title=request.title,
        description=request.description,
        task_type=request.task_type.value if request.task_type else TaskType.CODE_ANALYSIS.value,
        status=TaskStatus.QUEUED.value,
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    logger.info(f"Created task {task.id} for project {project_id}")
    
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        task_type=task.task_type,
        status=task.status,
        current_agent=task.current_agent,
        progress_percent=task.progress_percent,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        error_message=task.error_message,
    )


@router.get("/{project_id}/ai/tasks", response_model=List[TaskResponse])
async def list_tasks(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all AI tasks for a project."""
    # Verify project ownership
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    tasks = db.query(AITask).filter_by(project_id=project_id).all()
    
    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            project_id=task.project_id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            current_agent=task.current_agent,
            progress_percent=task.progress_percent,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            error_message=task.error_message,
        )
        for task in tasks
    ]


@router.get("/{project_id}/ai/tasks/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    project_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed task information."""
    task = db.query(AITask).filter_by(
        id=task_id,
        project_id=project_id,
        user_id=current_user.id,
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get executions
    executions = db.query(AgentExecution).filter_by(task_id=task_id).all()
    execution_responses = [
        {
            "id": ex.id,
            "agent_name": ex.agent_name,
            "status": ex.status,
            "input_summary": ex.input_summary,
            "output_summary": ex.output_summary,
            "tool_calls": ex.tool_calls,
            "tokens_used": ex.tokens_used,
            "started_at": ex.started_at,
            "completed_at": ex.completed_at,
            "duration_seconds": ex.duration_seconds,
            "error_message": ex.error_message,
        }
        for ex in executions
    ]
    
    return TaskDetailResponse(
        id=task.id,
        user_id=task.user_id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        task_type=task.task_type,
        status=task.status,
        current_agent=task.current_agent,
        progress_percent=task.progress_percent,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        error_message=task.error_message,
        agent_executions=execution_responses,
    )


@router.post("/{project_id}/ai/tasks/{task_id}/approve")
async def approve_task(
    project_id: int,
    task_id: int,
    approval: TaskApprovalRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Approve or reject a task.
    
    POST /api/v1/projects/{project_id}/ai/tasks/{task_id}/approve
    {
        "action": "APPROVED",
        "comment": "Looks good to merge"
    }
    """
    task = db.query(AITask).filter_by(
        id=task_id,
        project_id=project_id,
        user_id=current_user.id,
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != TaskStatus.WAITING_FOR_APPROVAL.value:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not waiting for approval (current status: {task.status})"
        )
    
    # Record approval
    approval_record = TaskApproval(
        task_id=task_id,
        user_id=current_user.id,
        action=approval.action,
        comment=approval.comment,
    )
    db.add(approval_record)
    
    # Update task status
    if approval.action == "APPROVED":
        task.status = TaskStatus.COMPLETED.value
    elif approval.action == "REJECTED":
        task.status = TaskStatus.FAILED.value
    
    db.commit()
    
    logger.info(f"Task {task_id} {approval.action} by user {current_user.id}")
    
    return {
        "status": task.status,
        "message": f"Approval recorded: {approval.action}",
    }


@router.post("/{project_id}/ai/tasks/{task_id}/cancel")
async def cancel_task(
    project_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel a running task."""
    task = db.query(AITask).filter_by(
        id=task_id,
        project_id=project_id,
        user_id=current_user.id,
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value, TaskStatus.CANCELLED.value]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel task in {task.status} state"
        )
    
    task.status = TaskStatus.CANCELLED.value
    db.commit()
    
    logger.info(f"Task {task_id} cancelled by user {current_user.id}")
    
    return {"status": "CANCELLED", "message": "Task cancelled"}
