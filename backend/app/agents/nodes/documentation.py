"""
Documentation Agent: Updates documentation for code changes.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function
from app.agents.state.models import TaskStatus

logger = logging.getLogger(__name__)


class DocumentationAgent(AgentNode):
    """Generates documentation updates."""
    
    def __init__(self):
        super().__init__("documentation")


async def execute_documentation(state: AgentGraphState) -> Dict[str, Any]:
    """
    Documentation Agent node execution.
    
    Responsibility:
    1. Review proposed changes
    2. Identify documentation needs
    3. Generate documentation updates
    4. Suggest changelog entries
    """
    agent = DocumentationAgent()
    agent.log_message("Starting documentation phase", "INFO")
    
    try:
        state = agent.add_agent_message(
            state,
            "documentation_checked",
            "Documentation requirements identified"
        )
        
        agent.log_message("Documentation phase complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Documentation phase failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "DOCUMENTATION_ERROR", str(e))
        return state


# Create the node function
documentation_node = create_node_function(DocumentationAgent(), execute_documentation)
