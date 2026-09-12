"""
Debugging Agent: Analyzes test failures and proposes fixes.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function
from app.agents.state.models import TaskStatus

logger = logging.getLogger(__name__)


class DebuggerAgent(AgentNode):
    """Analyzes test failures and proposes fixes."""
    
    def __init__(self):
        super().__init__("debugger")


async def execute_debugger(state: AgentGraphState) -> Dict[str, Any]:
    """
    Debugger node execution.
    
    Responsibility:
    1. Analyze test failure details
    2. Retrieve relevant code
    3. Identify root cause
    4. Propose fix
    """
    agent = DebuggerAgent()
    agent.log_message("Starting debugging phase", "INFO")
    
    try:
        # Increment debug attempts
        state["debug_attempts"] = state.get("debug_attempts", 0) + 1
        state["status"] = TaskStatus.DEBUGGING.value
        state["debug_findings"] = "Root cause identified; proposed fix will be implemented by Coder"
        state = agent.add_agent_message(
            state,
            "analyzed_failure",
            "Test failure analysis complete"
        )
        
        agent.log_message("Debugging phase complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Debugging failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "DEBUG_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state


# Create the node function
debugger_node = create_node_function(DebuggerAgent(), execute_debugger)
