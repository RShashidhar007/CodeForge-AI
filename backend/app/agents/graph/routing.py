"""
Conditional edge routing functions for LangGraph workflow.
Determines the next node based on current state and results.
"""
from typing import Literal
from app.agents.graph.state import AgentGraphState


def route_after_planning(state: AgentGraphState) -> Literal["explain_only", "analyze_only", "security_analysis", "code_change"]:
    """
    Route after Planner agent executes.
    Determines next step based on task type.
    """
    task_type = state.get("task_type", "CODE_ANALYSIS")
    
    if task_type == "CODE_EXPLANATION":
        return "explain_only"
    elif task_type == "CODE_ANALYSIS":
        return "analyze_only"
    elif task_type == "SECURITY_ANALYSIS":
        return "security_analysis"
    else:
        # BUG_FIX, CODE_IMPROVEMENT, TEST_GENERATION, FEATURE_IMPLEMENTATION, REFACTORING
        return "code_change"


def route_after_analysis(state: AgentGraphState) -> Literal["analysis_complete", "proceed_to_coding", "security_check"]:
    """
    Route after Analyzer agent executes.
    Check for security concerns or proceed to coding.
    """
    task_type = state.get("task_type", "CODE_ANALYSIS")
    
    # Analysis-only tasks end here
    if task_type == "CODE_ANALYSIS":
        return "analysis_complete"
    
    # Check for high-risk issues
    analysis_result = state.get("analysis_result")
    if analysis_result and analysis_result.risks:
        for risk in analysis_result.risks:
            if risk.get("severity") == "HIGH" or risk.get("severity") == "CRITICAL":
                return "security_check"
    
    # Proceed to coding
    return "proceed_to_coding"


def route_after_coder(state: AgentGraphState) -> Literal["review"]:
    """
    Route after Coder agent executes.
    Always goes to review.
    """
    return "review"


def route_after_review(state: AgentGraphState) -> Literal["approved", "changes_required", "rejected"]:
    """
    Route after Code Review agent executes.
    Based on review decision and iteration limits.
    """
    review_results = state.get("review_results")
    if not review_results:
        return "rejected"
    
    review_iteration = state.get("review_iteration", 0)
    max_review_iterations = state.get("max_review_iterations", 3)
    
    if review_results.approval == "APPROVED":
        return "approved"
    elif review_results.approval == "CHANGES_REQUIRED":
        if review_iteration < max_review_iterations:
            return "changes_required"
        else:
            # Max iterations reached
            return "rejected"
    else:
        return "rejected"


def route_after_testing(state: AgentGraphState) -> Literal["passed", "failed"]:
    """
    Route after Testing agent executes.
    Based on test results.
    """
    test_results = state.get("test_results")
    if test_results and test_results.success:
        return "passed"
    return "failed"


def route_after_debugging(state: AgentGraphState) -> Literal["retry_coding", "give_up"]:
    """
    Route after Debugging agent executes.
    Decide whether to retry or give up based on attempt limits.
    """
    debug_attempts = state.get("debug_attempts", 0)
    max_debug_attempts = state.get("max_debug_attempts", 3)
    
    if debug_attempts < max_debug_attempts:
        return "retry_coding"
    else:
        return "give_up"


def route_after_security_check(state: AgentGraphState) -> Literal["blocked", "proceed_to_approval"]:
    """
    Route after Security agent executes.
    Based on security findings severity.
    """
    analysis_result = state.get("analysis_result")
    if not analysis_result:
        return "proceed_to_approval"
    
    # Check for CRITICAL security issues
    for risk in analysis_result.risks:
        if risk.get("severity") == "CRITICAL":
            return "blocked"
    
    return "proceed_to_approval"


def route_to_final_approval(state: AgentGraphState) -> Literal["waiting_for_approval", "end"]:
    """
    Route to approval gate.
    Always returns waiting_for_approval to pause for human decision.
    """
    return "waiting_for_approval"


def route_after_approval(state: AgentGraphState) -> Literal["end"]:
    """
    Route after approval decision.
    All paths lead to end (workspace cleanup handled elsewhere).
    """
    return "end"


# ===== End node detection =====

def should_end_workflow(state: AgentGraphState) -> bool:
    """Check if workflow should terminate."""
    status = state.get("status", "QUEUED")
    terminal_statuses = ["COMPLETED", "FAILED", "CANCELLED"]
    return status in terminal_statuses
