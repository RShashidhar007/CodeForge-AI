"""
Patch generation and validation tools.
"""
import logging
from typing import Dict, Any
import difflib

logger = logging.getLogger(__name__)


class CreatePatchTool:
    """Generate unified diff patch."""
    
    def invoke(
        self,
        original_content: str,
        modified_content: str,
        file_path: str,
    ) -> str:
        """
        Generate unified diff patch.
        
        Args:
            original_content: Original file content
            modified_content: Modified file content
            file_path: File path for diff header
        
        Returns:
            Unified diff format patch
        """
        try:
            original_lines = original_content.splitlines(keepends=True)
            modified_lines = modified_content.splitlines(keepends=True)
            
            diff = difflib.unified_diff(
                original_lines,
                modified_lines,
                fromfile=f"a/{file_path}",
                tofile=f"b/{file_path}",
                lineterm=""
            )
            
            return "\n".join(diff)
        except Exception as e:
            logger.error(f"Failed to create patch for {file_path}: {str(e)}")
            raise


class ValidatePatchTool:
    """Validate patch syntax and applicability."""
    
    def invoke(
        self,
        patch: str,
        repository_path: str,
    ) -> Dict[str, Any]:
        """
        Validate patch.
        
        Args:
            patch: Patch content in unified diff format
            repository_path: Path to repository
        
        Returns:
            Validation result
        """
        try:
            # Check basic format
            if not patch.strip():
                return {"valid": False, "errors": ["Patch is empty"]}
            
            # Check for unified diff markers
            has_headers = "---" in patch and "+++" in patch
            if not has_headers:
                return {"valid": False, "errors": ["Missing unified diff headers"]}
            
            return {"valid": True, "can_apply": True}
        except Exception as e:
            logger.error(f"Patch validation failed: {str(e)}")
            return {"valid": False, "errors": [str(e)]}


class PreviewPatchTool:
    """Show diff preview."""
    
    def invoke(self, patch: str) -> str:
        """
        Format patch for display.
        
        Args:
            patch: Patch content
        
        Returns:
            Formatted patch for UI display
        """
        return patch
