"""
Approval Gate: Marks task as waiting for human approval.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode
from app.agents.state.models import TaskStatus

logger = logging.getLogger(__name__)


class ApprovalGateAgent(AgentNode):
    """Approval gate for human decision."""
    
    def __init__(self):
        super().__init__("approval_gate")


async def approval_gate_node(state: AgentGraphState) -> Dict[str, Any]:
    """
    Approval gate node execution.
    
    Marks task as waiting for human approval.
    Frontend will handle user interaction outside the graph.
    """
    agent = ApprovalGateAgent()
    agent.log_message("Workflow paused at approval gate", "INFO")
    
    try:
        state["status"] = TaskStatus.WAITING_FOR_APPROVAL.value
        state["approval_status"] = "PENDING"
        state = agent.add_agent_message(
            state,
            "waiting_for_approval",
            "Awaiting user approval before applying changes"
        )
        
        agent.log_message("Awaiting user approval", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Approval gate failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "APPROVAL_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state
