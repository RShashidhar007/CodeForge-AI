"""
Pydantic models for agent state, task execution, and results.
These define the structured data flow through the agent graph.
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TaskType(str, Enum):
    """Classification of AI tasks."""
    CODE_EXPLANATION = "CODE_EXPLANATION"
    CODE_ANALYSIS = "CODE_ANALYSIS"
    BUG_FIX = "BUG_FIX"
    CODE_IMPROVEMENT = "CODE_IMPROVEMENT"
    TEST_GENERATION = "TEST_GENERATION"
    FEATURE_IMPLEMENTATION = "FEATURE_IMPLEMENTATION"
    SECURITY_ANALYSIS = "SECURITY_ANALYSIS"
    REFACTORING = "REFACTORING"


class TaskStatus(str, Enum):
    """Status throughout task lifecycle."""
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    ANALYZING = "ANALYZING"
    CODING = "CODING"
    REVIEWING = "REVIEWING"
    TESTING = "TESTING"
    DEBUGGING = "DEBUGGING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ExecutionPlan(BaseModel):
    """Structured plan output from Planner agent."""
    goal: str = Field(..., description="Overall objective")
    steps: List[Dict[str, Any]] = Field(default_factory=list, description="Execution steps")
    estimated_duration_minutes: Optional[int] = Field(None, description="Time estimate")
    risk_level: str = Field(default="MEDIUM", description="Risk assessment: LOW/MEDIUM/HIGH")
    security_considerations: List[str] = Field(default_factory=list, description="Security notes")


class AnalysisResult(BaseModel):
    """Findings from Code Analysis agent."""
    relevant_files: List[str] = Field(default_factory=list, description="Files to analyze")
    key_functions: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Key functions/classes identified"
    )
    dependencies: List[str] = Field(default_factory=list, description="External dependencies")
    implementation_locations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Where to make changes"
    )
    risks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Identified risks: [{type, description, severity}]"
    )
    recommendations: str = Field(default="", description="Implementation recommendations")


class ProposedPatch(BaseModel):
    """Code patch from Coding agent."""
    affected_files: List[str] = Field(default_factory=list, description="Files modified")
    unified_diff: str = Field(default="", description="Unified diff format patch")
    change_summary: str = Field(default="", description="High-level summary of changes")
    implementation_notes: str = Field(default="", description="Implementation details")


class ReviewResult(BaseModel):
    """Code review from Review agent."""
    approval: str = Field(
        default="CHANGES_REQUIRED",
        description="APPROVED / CHANGES_REQUIRED / REJECTED"
    )
    issues: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Found issues: [{type, severity, description, location}]"
    )
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    test_coverage_assessment: str = Field(default="", description="Test coverage notes")
    security_issues: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Security findings: [{description, severity, recommendation}]"
    )


class TestResult(BaseModel):
    """Test execution results."""
    success: bool = Field(default=False, description="All tests passed")
    exit_code: int = Field(default=1, description="Exit code from test runner")
    stdout: str = Field(default="", description="Test output")
    stderr: str = Field(default="", description="Error output")
    duration_seconds: float = Field(default=0.0, description="Execution time")
    passed_count: int = Field(default=0, description="Number of passed tests")
    failed_count: int = Field(default=0, description="Number of failed tests")
    failures: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Failure details: [{test_name, error_message, stack_trace}]"
    )


class TaskState(BaseModel):
    """Complete state for agent graph execution."""
    
    # ===== Core Identifiers =====
    task_id: int = Field(..., description="Unique task ID")
    user_id: int = Field(..., description="Task creator user ID")
    project_id: int = Field(..., description="Target project ID")
    
    # ===== Task Definition =====
    user_request: str = Field(..., description="Original user request")
    task_type: TaskType = Field(default=TaskType.CODE_ANALYSIS, description="Type of task")
    title: str = Field(default="", description="Task title")
    description: str = Field(default="", description="Task description")
    selected_files: Optional[List[str]] = Field(default=None, description="Files to focus on")
    additional_context: Optional[str] = Field(None, description="Extra context from user")
    
    # ===== Execution State =====
    status: TaskStatus = Field(default=TaskStatus.QUEUED, description="Current task status")
    current_step: int = Field(default=0, description="Current execution step")
    current_agent: Optional[str] = Field(None, description="Currently executing agent")
    
    # ===== Planning Phase =====
    execution_plan: Optional[ExecutionPlan] = Field(None, description="Plan from Planner agent")
    
    # ===== Analysis Phase =====
    analysis_result: Optional[AnalysisResult] = Field(None, description="Analysis findings")
    retrieved_context: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="RAG-retrieved context"
    )
    
    # ===== Coding Phase =====
    proposed_patch: Optional[ProposedPatch] = Field(None, description="Proposed changes")
    patch_validation_errors: Optional[List[str]] = Field(
        None,
        description="Validation errors"
    )
    
    # ===== Review Phase =====
    review_results: Optional[ReviewResult] = Field(None, description="Code review results")
    review_iteration: int = Field(default=0, description="Review iteration count")
    max_review_iterations: int = Field(default=3, description="Max review retries")
    
    # ===== Testing Phase =====
    test_results: Optional[TestResult] = Field(None, description="Test execution results")
    test_iteration: int = Field(default=0, description="Test iteration count")
    max_test_iterations: int = Field(default=3, description="Max test retries")
    
    # ===== Debugging Phase =====
    debug_attempts: int = Field(default=0, description="Debug attempt count")
    max_debug_attempts: int = Field(default=3, description="Max debug retries")
    debug_findings: Optional[str] = Field(None, description="Debugging discoveries")
    
    # ===== Approval Phase =====
    approval_status: Optional[str] = Field(
        None,
        description="PENDING / APPROVED / REJECTED"
    )
    approval_comment: Optional[str] = Field(None, description="User approval comment")
    
    # ===== Tracking & History =====
    agent_messages: List[Dict[str, str]] = Field(
        default_factory=list,
        description="History: [{agent, action, result}]"
    )
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Accumulated errors"
    )
    
    # ===== Metadata =====
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    started_at: Optional[datetime] = Field(None, description="Execution start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    
    # ===== Workspace =====
    workspace_id: Optional[str] = Field(None, description="Working space identifier")
    branch_name: Optional[str] = Field(None, description="Git branch name")
    
    class Config:
        """Pydantic config."""
        use_enum_values = False


class AgentConfig(BaseModel):
    """Configuration for agent behavior."""
    max_iterations: int = Field(default=3, description="Max iterations")
    max_tool_calls: int = Field(default=50, description="Max tool invocations")
    timeout_seconds: int = Field(default=300, description="Execution timeout")
    retry_on_failure: bool = Field(default=True, description="Auto-retry on failure")
    use_mock_mode: bool = Field(default=False, description="Use mock LLM")


class ToolPermission(BaseModel):
    """Permissions for agent tool usage."""
    agent_name: str = Field(..., description="Agent name")
    allowed_tools: List[str] = Field(default_factory=list, description="Allowed tools")
    
    @staticmethod
    def get_permissions(agent_name: str) -> "ToolPermission":
        """Get tool permissions for an agent."""
        permissions_map = {
            "planner": ToolPermission(
                agent_name="planner",
                allowed_tools=["rag_search", "repository_read", "list_files"]
            ),
            "analyzer": ToolPermission(
                agent_name="analyzer",
                allowed_tools=[
                    "repository_read", "rag_search", "list_files", "search_code",
                    "inspect_function", "inspect_class", "inspect_dependencies"
                ]
            ),
            "coder": ToolPermission(
                agent_name="coder",
                allowed_tools=["repository_read", "create_patch", "validate_patch"]
            ),
            "reviewer": ToolPermission(
                agent_name="reviewer",
                allowed_tools=["repository_read", "preview_patch", "analyze_patch"]
            ),
            "tester": ToolPermission(
                agent_name="tester",
                allowed_tools=[
                    "repository_read", "run_tests", "run_specific_test",
                    "inspect_test_results"
                ]
            ),
            "debugger": ToolPermission(
                agent_name="debugger",
                allowed_tools=[
                    "repository_read", "create_patch", "validate_patch",
                    "run_tests", "run_specific_test"
                ]
            ),
            "security": ToolPermission(
                agent_name="security",
                allowed_tools=[
                    "repository_read", "rag_search", "list_files", "search_code",
                    "inspect_function", "inspect_class"
                ]
            ),
            "documentation": ToolPermission(
                agent_name="documentation",
                allowed_tools=["repository_read", "preview_patch"]
            ),
        }
        return permissions_map.get(
            agent_name,
            ToolPermission(agent_name=agent_name, allowed_tools=[])
        )


# ===== API Request/Response Models =====

class CreateTaskRequest(BaseModel):
    """Request to create a new AI task."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    task_type: Optional[TaskType] = Field(None, description="Task type hint")
    selected_files: Optional[List[str]] = Field(None, description="Focus on these files")
    additional_context: Optional[str] = Field(None, description="Extra context")


class TaskResponse(BaseModel):
    """Response for task query."""
    id: int = Field(..., description="Task ID")
    user_id: int = Field(..., description="Creator ID")
    project_id: int = Field(..., description="Project ID")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    task_type: str = Field(..., description="Task type")
    status: str = Field(..., description="Current status")
    current_agent: Optional[str] = Field(None, description="Currently executing agent")
    progress_percent: int = Field(default=0, description="Progress %")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    error_message: Optional[str] = Field(None, description="Error if failed")


class TaskDetailResponse(TaskResponse):
    """Extended response with execution history."""
    execution_plan: Optional[Dict[str, Any]] = Field(None, description="Planner output")
    analysis_result: Optional[Dict[str, Any]] = Field(None, description="Analysis findings")
    proposed_patch: Optional[Dict[str, Any]] = Field(None, description="Proposed changes")
    review_results: Optional[Dict[str, Any]] = Field(None, description="Review outcome")
    test_results: Optional[Dict[str, Any]] = Field(None, description="Test results")
    agent_executions: List[Dict[str, Any]] = Field(default_factory=list, description="Agent history")


class TaskApprovalRequest(BaseModel):
    """Request to approve or reject task."""
    action: str = Field(..., description="APPROVED / REJECTED / REQUESTED_CHANGES")
    comment: Optional[str] = Field(None, description="Approval comment")


class AgentExecutionResponse(BaseModel):
    """Response for agent execution record."""
    id: int = Field(..., description="Execution ID")
    task_id: int = Field(..., description="Task ID")
    agent_name: str = Field(..., description="Agent name")
    status: str = Field(..., description="Execution status")
    input_summary: Optional[str] = Field(None, description="Input summary")
    output_summary: Optional[str] = Field(None, description="Output summary")
    tool_calls: int = Field(default=0, description="Tools invoked")
    tokens_used: Optional[int] = Field(None, description="Tokens consumed")
    started_at: datetime = Field(..., description="Start time")
    completed_at: Optional[datetime] = Field(None, description="End time")
    duration_seconds: Optional[float] = Field(None, description="Execution duration")
    error_message: Optional[str] = Field(None, description="Error if failed")


class PatchResponse(BaseModel):
    """Response for patch record."""
    id: int = Field(..., description="Patch ID")
    task_id: int = Field(..., description="Task ID")
    agent_id: Optional[str] = Field(None, description="Agent that created patch")
    target_files: List[str] = Field(default_factory=list, description="Files affected")
    patch_content: str = Field(default="", description="Unified diff")
    validation_status: str = Field(..., description="Validation status")
    review_status: Optional[str] = Field(None, description="Review status")
    created_at: datetime = Field(..., description="Creation time")


class ProgressUpdate(BaseModel):
    """WebSocket progress update."""
    task_id: int = Field(..., description="Task ID")
    status: str = Field(..., description="Current status")
    current_agent: Optional[str] = Field(None, description="Current agent")
    progress_percent: int = Field(default=0, description="Progress %")
    message: Optional[str] = Field(None, description="Status message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Update time")
