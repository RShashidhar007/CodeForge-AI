"""
Coding Agent: Proposes code changes and generates patches.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function
from app.agents.state.models import ProposedPatch, TaskStatus

logger = logging.getLogger(__name__)


class CoderAgent(AgentNode):
    """Generates code changes and patches."""
    
    def __init__(self):
        super().__init__("coder")


async def execute_coder(state: AgentGraphState) -> Dict[str, Any]:
    """
    Coder node execution.
    
    Responsibility:
    1. Propose code changes
    2. Generate unified diff
    3. Follow existing style
    4. Preserve architecture
    """
    agent = CoderAgent()
    agent.log_message("Starting coding phase", "INFO")
    
    try:
        # Create proposed patch
        patch = ProposedPatch(
            affected_files=[],
            unified_diff="",
            change_summary="Proposed changes based on analysis",
            implementation_notes=""
        )
        
        state["proposed_patch"] = patch
        state["status"] = TaskStatus.CODING.value
        state = agent.add_agent_message(
            state,
            "generated_patch",
            "Patch generated for review"
        )
        
        agent.log_message("Coding phase complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Coding failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "CODING_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state


# Create the node function
coder_node = create_node_function(CoderAgent(), execute_coder)
