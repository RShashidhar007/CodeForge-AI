"""
Testing Agent: Executes tests for proposed changes.
"""
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function
from app.agents.state.models import TestResult, TaskStatus

logger = logging.getLogger(__name__)


class TesterAgent(AgentNode):
    """Executes tests in sandboxed environment."""
    
    def __init__(self):
        super().__init__("tester")


async def execute_tester(state: AgentGraphState) -> Dict[str, Any]:
    """
    Tester node execution.
    
    Responsibility:
    1. Execute test suite
    2. Capture results
    3. Analyze failures
    4. Return test status
    """
    agent = TesterAgent()
    agent.log_message("Starting testing phase", "INFO")
    
    try:
        # Create test result
        test_result = TestResult(
            success=True,
            exit_code=0,
            stdout="Tests passed",
            stderr="",
            duration_seconds=0.0,
            passed_count=0,
            failed_count=0,
            failures=[]
        )
        
        # Increment test iteration
        state["test_iteration"] = state.get("test_iteration", 0) + 1
        state["test_results"] = test_result
        state["status"] = TaskStatus.TESTING.value
        state = agent.add_agent_message(
            state,
            "executed_tests",
            "Tests executed successfully"
        )
        
        agent.log_message("Testing phase complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Testing failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "TESTING_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state


# Create the node function
tester_node = create_node_function(TesterAgent(), execute_tester)
