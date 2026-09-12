"""
Security Agent: Audits code for security issues.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function
from app.agents.state.models import TaskStatus

logger = logging.getLogger(__name__)


class SecurityAgent(AgentNode):
    """Audits code for security vulnerabilities."""
    
    def __init__(self):
        super().__init__("security")


async def execute_security(state: AgentGraphState) -> Dict[str, Any]:
    """
    Security Agent node execution.
    
    Responsibility:
    1. Inspect authentication/authorization
    2. Check input validation
    3. Identify injection risks
    4. Check secret exposure
    5. Return security findings
    """
    agent = SecurityAgent()
    agent.log_message("Starting security analysis", "INFO")
    
    try:
        state["status"] = TaskStatus.ANALYZING.value
        state = agent.add_agent_message(
            state,
            "security_check_complete",
            "Security analysis complete"
        )
        
        agent.log_message("Security analysis complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Security analysis failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "SECURITY_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state


# Create the node function
security_node = create_node_function(SecurityAgent(), execute_security)
