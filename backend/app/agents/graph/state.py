"""
LangGraph state definition and management for the agent workflow.
"""
from typing import TypedDict, Optional, List, Dict, Any
from app.agents.state.models import (
    TaskState,
    ExecutionPlan,
    AnalysisResult,
    ProposedPatch,
    ReviewResult,
    TestResult,
)


class AgentGraphState(TypedDict, total=False):
    """
    TypedDict for LangGraph state.
    Represents the complete state passed between agent nodes.
    
    TypedDict with total=False means all fields are optional,
    which allows agents to only update the fields they care about.
    """
    
    # Core identifiers
    task_id: int
    user_id: int
    project_id: int
    
    # Task definition
    user_request: str
    task_type: str
    title: str
    description: str
    selected_files: Optional[List[str]]
    additional_context: Optional[str]
    
    # Execution state
    status: str
    current_step: int
    current_agent: Optional[str]
    
    # Planning phase
    execution_plan: Optional[ExecutionPlan]
    
    # Analysis phase
    analysis_result: Optional[AnalysisResult]
    retrieved_context: Optional[List[Dict[str, Any]]]
    
    # Coding phase
    proposed_patch: Optional[ProposedPatch]
    patch_validation_errors: Optional[List[str]]
    
    # Review phase
    review_results: Optional[ReviewResult]
    review_iteration: int
    max_review_iterations: int
    
    # Testing phase
    test_results: Optional[TestResult]
    test_iteration: int
    max_test_iterations: int
    
    # Debugging phase
    debug_attempts: int
    max_debug_attempts: int
    debug_findings: Optional[str]
    
    # Approval phase
    approval_status: Optional[str]
    approval_comment: Optional[str]
    
    # Tracking
    agent_messages: List[Dict[str, str]]
    errors: List[Dict[str, Any]]
    
    # Metadata
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    
    # Workspace
    workspace_id: Optional[str]
    branch_name: Optional[str]


def create_initial_state(task_state: TaskState) -> AgentGraphState:
    """Convert TaskState to AgentGraphState for graph execution."""
    return {
        "task_id": task_state.task_id,
        "user_id": task_state.user_id,
        "project_id": task_state.project_id,
        "user_request": task_state.user_request,
        "task_type": task_state.task_type.value,
        "title": task_state.title,
        "description": task_state.description,
        "selected_files": task_state.selected_files,
        "additional_context": task_state.additional_context,
        "status": task_state.status.value,
        "current_step": task_state.current_step,
        "current_agent": task_state.current_agent,
        "execution_plan": task_state.execution_plan,
        "analysis_result": task_state.analysis_result,
        "retrieved_context": task_state.retrieved_context,
        "proposed_patch": task_state.proposed_patch,
        "patch_validation_errors": task_state.patch_validation_errors,
        "review_results": task_state.review_results,
        "review_iteration": task_state.review_iteration,
        "max_review_iterations": task_state.max_review_iterations,
        "test_results": task_state.test_results,
        "test_iteration": task_state.test_iteration,
        "max_test_iterations": task_state.max_test_iterations,
        "debug_attempts": task_state.debug_attempts,
        "max_debug_attempts": task_state.max_debug_attempts,
        "debug_findings": task_state.debug_findings,
        "approval_status": task_state.approval_status,
        "approval_comment": task_state.approval_comment,
        "agent_messages": task_state.agent_messages,
        "errors": task_state.errors,
        "created_at": task_state.created_at.isoformat(),
        "started_at": task_state.started_at.isoformat() if task_state.started_at else None,
        "completed_at": task_state.completed_at.isoformat() if task_state.completed_at else None,
        "workspace_id": task_state.workspace_id,
        "branch_name": task_state.branch_name,
    }


def state_to_task_state(state: AgentGraphState) -> TaskState:
    """Convert AgentGraphState back to TaskState."""
    from datetime import datetime
    
    return TaskState(
        task_id=state.get("task_id", 0),
        user_id=state.get("user_id", 0),
        project_id=state.get("project_id", 0),
        user_request=state.get("user_request", ""),
        task_type=state.get("task_type", "CODE_ANALYSIS"),
        title=state.get("title", ""),
        description=state.get("description", ""),
        selected_files=state.get("selected_files"),
        additional_context=state.get("additional_context"),
        status=state.get("status", "QUEUED"),
        current_step=state.get("current_step", 0),
        current_agent=state.get("current_agent"),
        execution_plan=state.get("execution_plan"),
        analysis_result=state.get("analysis_result"),
        retrieved_context=state.get("retrieved_context"),
        proposed_patch=state.get("proposed_patch"),
        patch_validation_errors=state.get("patch_validation_errors"),
        review_results=state.get("review_results"),
        review_iteration=state.get("review_iteration", 0),
        max_review_iterations=state.get("max_review_iterations", 3),
        test_results=state.get("test_results"),
        test_iteration=state.get("test_iteration", 0),
        max_test_iterations=state.get("max_test_iterations", 3),
        debug_attempts=state.get("debug_attempts", 0),
        max_debug_attempts=state.get("max_debug_attempts", 3),
        debug_findings=state.get("debug_findings"),
        approval_status=state.get("approval_status"),
        approval_comment=state.get("approval_comment"),
        agent_messages=state.get("agent_messages", []),
        errors=state.get("errors", []),
        created_at=datetime.fromisoformat(state.get("created_at", datetime.utcnow().isoformat())),
        started_at=datetime.fromisoformat(state["started_at"]) if state.get("started_at") else None,
        completed_at=datetime.fromisoformat(state["completed_at"]) if state.get("completed_at") else None,
        workspace_id=state.get("workspace_id"),
        branch_name=state.get("branch_name"),
    )
