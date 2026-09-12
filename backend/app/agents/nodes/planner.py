"""
Planner Agent: Understands user request and creates execution plan.
"""
import json
import logging
from typing import Dict, Any
from app.agents.graph.state import AgentGraphState
from app.agents.nodes.base import AgentNode, create_node_function, extract_json_from_response
from app.agents.state.models import ExecutionPlan, TaskStatus

logger = logging.getLogger(__name__)


class PlannerAgent(AgentNode):
    """Plans AI task execution based on user request."""
    
    def __init__(self):
        super().__init__("planner")


async def execute_planner(state: AgentGraphState) -> Dict[str, Any]:
    """
    Planner node execution.
    
    Responsibility:
    1. Understand user request
    2. Determine task type
    3. Identify relevant files
    4. Break into steps
    5. Return execution plan
    """
    agent = PlannerAgent()
    agent.log_message("Starting planning phase", "INFO")
    
    try:
        # Extract task info from state
        user_request = state.get("user_request", "")
        task_type = state.get("task_type", "CODE_ANALYSIS")
        project_id = state.get("project_id", 0)
        
        # For now, create a basic plan
        # In full implementation, this would call LLM with prompts
        plan = ExecutionPlan(
            goal=user_request,
            steps=[
                {
                    "id": 1,
                    "description": "Analyze repository and identify relevant code",
                    "agent": "analyzer",
                    "dependencies": []
                },
                {
                    "id": 2,
                    "description": "Implement changes if code modification is needed",
                    "agent": "coder",
                    "dependencies": [1]
                },
                {
                    "id": 3,
                    "description": "Review code changes for quality and security",
                    "agent": "reviewer",
                    "dependencies": [2]
                },
                {
                    "id": 4,
                    "description": "Execute tests to verify changes",
                    "agent": "tester",
                    "dependencies": [3]
                }
            ],
            risk_level="MEDIUM",
            security_considerations=["Input validation", "Error handling", "No secrets in output"]
        )
        
        state["execution_plan"] = plan
        state["status"] = TaskStatus.PLANNING.value
        state = agent.add_agent_message(
            state,
            "created_plan",
            f"Plan created with {len(plan.steps)} steps"
        )
        
        agent.log_message("Planning phase complete", "INFO")
        return state
        
    except Exception as e:
        agent.log_message(f"Planning failed: {str(e)}", "ERROR")
        state = agent.add_error(state, "PLANNING_ERROR", str(e))
        state["status"] = TaskStatus.FAILED.value
        return state


# Create the node function
planner_node = create_node_function(PlannerAgent(), execute_planner)
