"""
Base classes and utilities for agent nodes.
"""
import logging
from typing import Any, Dict, Optional, Callable
from datetime import datetime
from app.agents.graph.state import AgentGraphState
from app.agents.state.models import TaskStatus

logger = logging.getLogger(__name__)


class AgentNode:
    """
    Base class for agent nodes.
    Provides common functionality for all agents.
    """
    
    def __init__(self, name: str):
        self.name = name
    
    def log_message(self, message: str, level: str = "INFO"):
        """Log agent activity."""
        getattr(logger, level.lower())(f"[{self.name}] {message}")
    
    def add_agent_message(
        self,
        state: AgentGraphState,
        action: str,
        result: str
    ) -> AgentGraphState:
        """Add message to agent_messages history."""
        if "agent_messages" not in state:
            state["agent_messages"] = []
        
        state["agent_messages"].append({
            "agent": self.name,
            "action": action,
            "result": result,
            "timestamp": datetime.utcnow().isoformat(),
        })
        return state
    
    def add_error(
        self,
        state: AgentGraphState,
        error_type: str,
        message: str
    ) -> AgentGraphState:
        """Add error to errors history."""
        if "errors" not in state:
            state["errors"] = []
        
        state["errors"].append({
            "agent": self.name,
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        })
        return state
    
    def update_status(
        self,
        state: AgentGraphState,
        status: str
    ) -> AgentGraphState:
        """Update task status."""
        state["status"] = status
        state["current_agent"] = self.name
        return state


def create_node_function(agent: AgentNode, execute_fn: Callable) -> Callable:
    """
    Create a node function for LangGraph.
    
    Args:
        agent: AgentNode instance
        execute_fn: Async function that implements agent logic
    
    Returns:
        Node function compatible with LangGraph
    """
    async def node_fn(state: AgentGraphState) -> Dict[str, Any]:
        """Execute agent node."""
        try:
            agent.log_message(f"Starting execution", "INFO")
            
            # Execute agent logic
            result = await execute_fn(state)
            
            agent.log_message(f"Completed successfully", "INFO")
            return result
        
        except Exception as e:
            error_msg = f"Execution failed: {str(e)}"
            agent.log_message(error_msg, "ERROR")
            
            # Add error to state
            state = agent.add_error(state, "EXECUTION_ERROR", str(e))
            state["status"] = TaskStatus.FAILED.value
            return state
    
    return node_fn


async def call_llm_with_fallback(
    llm_provider,
    prompt: str,
    agent_name: str,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    fallback_response: Optional[str] = None,
) -> str:
    """
    Call LLM with error handling and fallback.
    
    Args:
        llm_provider: LLM provider instance
        prompt: Prompt to send to LLM
        agent_name: Name of calling agent (for logging)
        temperature: Optional temperature override
        max_tokens: Optional max tokens override
        fallback_response: Response to return if LLM fails
    
    Returns:
        LLM response or fallback response
    """
    try:
        response = await llm_provider.generate_response(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response
    except Exception as e:
        logger.error(f"[{agent_name}] LLM call failed: {str(e)}")
        
        if fallback_response:
            logger.warning(f"[{agent_name}] Using fallback response")
            return fallback_response
        
        raise


def extract_json_from_response(response: str, fallback: Optional[Dict] = None) -> Dict:
    """
    Extract JSON from LLM response.
    LLM often wraps JSON in markdown code blocks.
    
    Args:
        response: LLM response text
        fallback: Dict to return if parsing fails
    
    Returns:
        Parsed JSON as dict
    """
    import json
    import re
    
    # Try direct JSON parsing first
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try extracting from markdown code block
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Fallback
    if fallback:
        return fallback
    
    raise ValueError("Could not extract JSON from LLM response")
