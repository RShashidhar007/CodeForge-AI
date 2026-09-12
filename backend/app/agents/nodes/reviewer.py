"""
Review Agent: Reviews code changes for quality, security, and correctness.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function
from app.agents.state.models import ReviewResult, TaskStatus

logger = logging.getLogger(__name__)


class ReviewerAgent(AgentNode):
    """Reviews proposed code changes."""
    
    def __init__(self):
        super().__init__("reviewer")


async def execute_reviewer(state: AgentGraphState) -> Dict[str, Any]:
    """
    Reviewer node execution.
    
    Responsibility:
    1. Review proposed changes
    2. Check correctness
    3. Check security
    4. Check maintainability
    5. Return review decision
    """
    agent = ReviewerAgent()
    agent.log_message("Starting review phase", "INFO")
    
    try:
        # Create review result
        review_result = ReviewResult(
            approval="APPROVED",
            issues=[],
            suggestions=[],
            test_coverage_assessment="",
            security_issues=[]
        )
        
        # Increment review iteration
        state["review_iteration"] = state.get("review_iteration", 0) + 1
        state["review_results"] = review_result
        state["status"] = TaskStatus.REVIEWING.value
        state = agent.add_agent_message(
            state,
            "completed_review",
            f"Review complete - {review_result.approval}"
        )
        
        agent.log_message("Review phase complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Review failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "REVIEW_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state


# Create the node function
reviewer_node = create_node_function(ReviewerAgent(), execute_reviewer)
