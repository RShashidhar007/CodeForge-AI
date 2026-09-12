"""
Cleanup Node: Finalizes task and cleans up resources.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode
from app.agents.state.models import TaskStatus

logger = logging.getLogger(__name__)


class CleanupAgent(AgentNode):
    """Cleanup and finalization agent."""
    
    def __init__(self):
        super().__init__("cleanup")


async def cleanup_node(state: AgentGraphState) -> Dict[str, Any]:
    """
    Cleanup node execution.
    
    Responsibility:
    1. Clean up workspaces
    2. Finalize task status
    3. Record completion
    """
    agent = CleanupAgent()
    agent.log_message("Starting cleanup phase", "INFO")
    
    try:
        # Mark task as completed or failed based on current status
        current_status = state.get("status", TaskStatus.FAILED.value)
        if current_status == TaskStatus.WAITING_FOR_APPROVAL.value:
            # If still waiting for approval, leave it as is
            final_status = current_status
        elif current_status == TaskStatus.FAILED.value:
            final_status = TaskStatus.FAILED.value
        else:
            # Successful completion path
            final_status = TaskStatus.COMPLETED.value
        
        state["status"] = final_status
        state = agent.add_agent_message(
            state,
            "cleanup_complete",
            f"Task {final_status}"
        )
        
        agent.log_message(f"Cleanup complete - Task {final_status}", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Cleanup failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "CLEANUP_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state
