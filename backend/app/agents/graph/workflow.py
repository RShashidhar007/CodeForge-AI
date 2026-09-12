"""
LangGraph workflow definition for the multi-agent AI system.
Builds and compiles the agent graph with all nodes and edges.
"""
import logging
from typing import Optional
from langgraph.graph import StateGraph, END

from app.agents.graph.state import AgentGraphState
from app.agents.graph.routing import (
    route_after_planning,
    route_after_analysis,
    route_after_coder,
    route_after_review,
    route_after_testing,
    route_after_debugging,
    route_after_security_check,
    route_to_final_approval,
    route_after_approval,
)

logger = logging.getLogger(__name__)


def build_agent_graph():
    """
    Build and compile the LangGraph agent workflow.
    
    Returns:
        Compiled StateGraph ready for invocation
    """
    workflow = StateGraph(AgentGraphState)
    
    # ===== Add Agent Nodes =====
    # Import agents here to avoid circular imports
    from app.agents.nodes.planner import planner_node
    from app.agents.nodes.analyzer import analyzer_node
    from app.agents.nodes.coder import coder_node
    from app.agents.nodes.reviewer import reviewer_node
    from app.agents.nodes.tester import tester_node
    from app.agents.nodes.debugger import debugger_node
    from app.agents.nodes.security import security_node
    from app.agents.nodes.documentation import documentation_node
    from app.agents.nodes.approval_gate import approval_gate_node
    from app.agents.nodes.cleanup import cleanup_node
    
    # Core agents
    workflow.add_node("planner", planner_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("debugger", debugger_node)
    
    # Specialized agents
    workflow.add_node("security", security_node)
    workflow.add_node("documentation", documentation_node)
    
    # Control flow nodes
    workflow.add_node("approval_gate", approval_gate_node)
    workflow.add_node("cleanup", cleanup_node)
    
    # ===== Set Entry Point =====
    workflow.set_entry_point("planner")
    
    # ===== Add Edges (Routing) =====
    
    # Planner routes to task-specific handler
    workflow.add_conditional_edges(
        "planner",
        route_after_planning,
        {
            "explain_only": "approval_gate",
            "analyze_only": "analyzer",
            "security_analysis": "security",
            "code_change": "analyzer",
        }
    )
    
    # Analyzer routes based on findings
    workflow.add_conditional_edges(
        "analyzer",
        route_after_analysis,
        {
            "analysis_complete": "approval_gate",
            "proceed_to_coding": "coder",
            "security_check": "security",
        }
    )
    
    # Coder always goes to review
    workflow.add_edge("coder", "reviewer")
    
    # Reviewer has conditional routing
    workflow.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "approved": "tester",
            "changes_required": "coder",
            "rejected": "cleanup",
        }
    )
    
    # Tester routes to debugging or approval
    workflow.add_conditional_edges(
        "tester",
        route_after_testing,
        {
            "passed": "approval_gate",
            "failed": "debugger",
        }
    )
    
    # Debugger routes back to coder or gives up
    workflow.add_conditional_edges(
        "debugger",
        route_after_debugging,
        {
            "retry_coding": "coder",
            "give_up": "cleanup",
        }
    )
    
    # Security analysis routes to approval or blocks
    workflow.add_conditional_edges(
        "security",
        route_after_security_check,
        {
            "blocked": "cleanup",
            "proceed_to_approval": "approval_gate",
        }
    )
    
    # Documentation and approval_gate both go to approval gate
    workflow.add_edge("documentation", "approval_gate")
    
    # Approval gate always returns waiting_for_approval state
    # (frontend will handle user interaction outside the graph)
    workflow.add_edge("approval_gate", END)
    
    # Cleanup always ends
    workflow.add_edge("cleanup", END)
    
    # ===== Compile Graph =====
    compiled_graph = workflow.compile()
    
    logger.info("Agent workflow compiled successfully")
    return compiled_graph


# Global compiled graph (lazy-loaded)
_graph: Optional[StateGraph] = None


def get_agent_graph():
    """Get or build the compiled agent graph."""
    global _graph
    if _graph is None:
        _graph = build_agent_graph()
    return _graph
