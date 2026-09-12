"""
Tool registry with permission-based access control.
"""
import logging
from typing import Any, Dict, List, Optional
from app.agents.state.models import ToolPermission

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Central registry of available tools with permission checking."""
    
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name: str, tool: Any):
        """Register a tool."""
        self.tools[name] = tool
        logger.info(f"Tool registered: {name}")
    
    @staticmethod
    def can_agent_use_tool(agent_name: str, tool_name: str) -> bool:
        """Check if agent has permission to use tool."""
        permissions = ToolPermission.get_permissions(agent_name)
        return tool_name in permissions.allowed_tools
    
    def invoke_tool(self, agent_name: str, tool_name: str, **kwargs) -> Any:
        """Invoke tool with permission check."""
        # Check permissions
        if not self.can_agent_use_tool(agent_name, tool_name):
            raise PermissionError(
                f"Agent {agent_name} cannot use tool {tool_name}"
            )
        
        # Get tool
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # Invoke
        logger.debug(f"[{agent_name}] Invoking tool: {tool_name}")
        return tool.invoke(**kwargs)
    
    def get_available_tools(self, agent_name: str) -> List[str]:
        """Get list of tools available to an agent."""
        permissions = ToolPermission.get_permissions(agent_name)
        return [t for t in permissions.allowed_tools if t in self.tools]


# Global registry
_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get or create global tool registry."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
        _initialize_tools(_registry)
    return _registry


def _initialize_tools(registry: ToolRegistry):
    """Initialize built-in tools."""
    from app.agents.tools.repository import RepositoryTool
    from app.agents.tools.patch import CreatePatchTool, ValidatePatchTool, PreviewPatchTool
    from app.agents.tools.test import RunTestsTool
    
    # Repository tools
    registry.register_tool("repository_read", RepositoryTool())
    registry.register_tool("list_files", RepositoryTool())
    
    # Patch tools
    registry.register_tool("create_patch", CreatePatchTool())
    registry.register_tool("validate_patch", ValidatePatchTool())
    registry.register_tool("preview_patch", PreviewPatchTool())
    
    # Test tools
    registry.register_tool("run_tests", RunTestsTool())
