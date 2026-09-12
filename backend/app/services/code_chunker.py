"""
Intelligent code chunking service.
Supports AST-based chunking for various languages and fallback strategies.
"""
import ast
import re
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CodeChunk:
    """Represents a chunk of code."""
    content: str
    start_line: int
    end_line: int
    symbol_name: Optional[str] = None  # Function/class name
    chunk_type: str = "code"  # "function", "class", "method", "module", etc.


class CodeChunker:
    """
    Intelligent code chunking using language-specific strategies.
    Falls back to fixed-size chunking for unsupported languages.
    """

    # Language to file extension mapping
    LANGUAGE_EXTENSIONS = {
        "python": [".py"],
        "javascript": [".js", ".jsx"],
        "typescript": [".ts", ".tsx"],
        "java": [".java"],
        "csharp": [".cs"],
        "cpp": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
        "c": [".c", ".h"],
        "go": [".go"],
        "rust": [".rs"],
        "ruby": [".rb"],
        "php": [".php"],
        "html": [".html", ".htm"],
        "css": [".css", ".scss", ".sass", ".less"],
        "sql": [".sql"],
        "json": [".json"],
        "yaml": [".yaml", ".yml"],
        "markdown": [".md", ".markdown"],
    }

    # Default chunk sizes (lines)
    CHUNK_SIZES = {
        "python": 50,
        "javascript": 50,
        "typescript": 50,
        "java": 60,
        "csharp": 60,
        "cpp": 70,
        "c": 70,
        "default": 100,
    }

    # Overlap between chunks (lines)
    OVERLAP = 5

    def __init__(self, max_chunk_size: int = 500, min_chunk_size: int = 50):
        """
        Initialize code chunker.

        Args:
            max_chunk_size: Maximum characters in a chunk
            min_chunk_size: Minimum characters in a chunk
        """
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

    def chunk_code(
        self,
        content: str,
        language: str,
        filepath: str = "",
    ) -> List[CodeChunk]:
        """
        Split code into semantic chunks.

        Args:
            content: Source code content
            language: Programming language
            filepath: File path (for context)

        Returns:
            List of CodeChunk objects
        """
        if not content.strip():
            return []

        # Try language-specific chunking
        if language.lower() == "python":
            return self._chunk_python(content)
        elif language.lower() in ["javascript", "typescript"]:
            return self._chunk_javascript(content, language)
        elif language.lower() == "java":
            return self._chunk_java(content)
        else:
            # Fall back to line-based chunking
            return self._chunk_generic(content, language)

    def _chunk_python(self, content: str) -> List[CodeChunk]:
        """
        Chunk Python code using AST (Abstract Syntax Tree).
        Identifies functions, classes, and methods.
        """
        chunks = []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.warning(f"Failed to parse Python code: {e}. Using fallback chunking.")
            return self._chunk_generic(content, "python")

        lines = content.split("\n")
        processed_lines = set()

        # Process top-level functions and classes
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chunk = self._extract_node_chunk(node, lines, "function")
                if chunk:
                    chunks.append(chunk)
                    processed_lines.update(range(node.lineno - 1, node.end_lineno or len(lines)))

            elif isinstance(node, ast.ClassDef):
                chunk = self._extract_node_chunk(node, lines, "class")
                if chunk:
                    chunks.append(chunk)
                    processed_lines.update(range(node.lineno - 1, node.end_lineno or len(lines)))

        # Add remaining code as generic chunks
        remaining_lines = []
        current_start = 0

        for i, line in enumerate(lines):
            if i not in processed_lines:
                remaining_lines.append((i, line))

        if remaining_lines:
            # Group remaining lines into chunks
            for chunk_lines in self._group_lines(remaining_lines, self.CHUNK_SIZES.get("python", 100)):
                if chunk_lines:
                    start_idx = chunk_lines[0][0]
                    end_idx = chunk_lines[-1][0]
                    chunk_content = "\n".join([line for _, line in chunk_lines])

                    if len(chunk_content.strip()) > self.min_chunk_size:
                        chunks.append(
                            CodeChunk(
                                content=chunk_content,
                                start_line=start_idx + 1,
                                end_line=end_idx + 1,
                                symbol_name=None,
                                chunk_type="module",
                            )
                        )

        return chunks

    def _chunk_javascript(self, content: str, language: str = "javascript") -> List[CodeChunk]:
        """
        Chunk JavaScript/TypeScript code using regex patterns.
        Identifies functions and arrow functions.
        """
        chunks = []
        lines = content.split("\n")

        # Patterns for functions, classes, async functions
        patterns = [
            (r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)", "function"),
            (r"^\s*(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s*)?\(", "function"),
            (r"^\s*(?:export\s+)?class\s+(\w+)", "class"),
            (r"^\s*(?:export\s+default\s+)?(?:async\s+)?function", "function"),
        ]

        i = 0
        while i < len(lines):
            line = lines[i]
            matched = False

            for pattern, chunk_type in patterns:
                match = re.match(pattern, line)
                if match:
                    symbol_name = match.group(1) if match.groups() else None
                    start_idx = i

                    # Find the end of this function/class
                    brace_count = line.count("{") - line.count("}")
                    end_idx = i

                    for j in range(i + 1, len(lines)):
                        brace_count += lines[j].count("{") - lines[j].count("}")
                        end_idx = j
                        if brace_count == 0 and "{" in "\n".join(lines[i : j + 1]):
                            break

                    chunk_content = "\n".join(lines[start_idx : end_idx + 1])

                    if len(chunk_content.strip()) > self.min_chunk_size:
                        chunks.append(
                            CodeChunk(
                                content=chunk_content,
                                start_line=start_idx + 1,
                                end_line=end_idx + 1,
                                symbol_name=symbol_name,
                                chunk_type=chunk_type,
                            )
                        )

                    i = end_idx + 1
                    matched = True
                    break

            if not matched:
                i += 1

        return chunks

    def _chunk_java(self, content: str) -> List[CodeChunk]:
        """
        Chunk Java code using regex patterns.
        Identifies classes, methods, and interfaces.
        """
        chunks = []
        lines = content.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]

            # Match class definitions
            if re.search(r"^\s*(?:public\s+)?(?:abstract\s+)?class\s+(\w+)", line):
                match = re.search(r"class\s+(\w+)", line)
                class_name = match.group(1) if match else None
                start_idx = i

                # Find class end
                brace_count = line.count("{") - line.count("}")
                end_idx = i

                for j in range(i + 1, len(lines)):
                    brace_count += lines[j].count("{") - lines[j].count("}")
                    end_idx = j
                    if brace_count == 0:
                        break

                chunk_content = "\n".join(lines[start_idx : end_idx + 1])

                if len(chunk_content.strip()) > self.min_chunk_size:
                    chunks.append(
                        CodeChunk(
                            content=chunk_content,
                            start_line=start_idx + 1,
                            end_line=end_idx + 1,
                            symbol_name=class_name,
                            chunk_type="class",
                        )
                    )

                i = end_idx + 1
            else:
                i += 1

        return chunks

    def _chunk_generic(self, content: str, language: str) -> List[CodeChunk]:
        """
        Generic line-based chunking for unsupported languages.
        Chunks by fixed number of lines.
        """
        chunks = []
        lines = content.split("\n")
        chunk_size = self.CHUNK_SIZES.get(language.lower(), self.CHUNK_SIZES["default"])

        for i in range(0, len(lines), chunk_size - self.OVERLAP):
            end_idx = min(i + chunk_size, len(lines))
            chunk_lines = lines[i:end_idx]
            chunk_content = "\n".join(chunk_lines)

            if len(chunk_content.strip()) > self.min_chunk_size:
                chunks.append(
                    CodeChunk(
                        content=chunk_content,
                        start_line=i + 1,
                        end_line=end_idx,
                        symbol_name=None,
                        chunk_type="module",
                    )
                )

        return chunks

    def _extract_node_chunk(
        self,
        node: ast.AST,
        lines: List[str],
        chunk_type: str,
    ) -> Optional[CodeChunk]:
        """
        Extract a chunk from an AST node.

        Args:
            node: AST node (FunctionDef, ClassDef, etc.)
            lines: Source code lines
            chunk_type: Type of chunk (function, class, etc.)

        Returns:
            CodeChunk object or None
        """
        try:
            start_line = node.lineno - 1
            end_line = node.end_lineno or len(lines)

            chunk_lines = lines[start_line:end_line]
            content = "\n".join(chunk_lines)

            # Get symbol name
            symbol_name = getattr(node, "name", None)

            if len(content.strip()) > self.min_chunk_size:
                return CodeChunk(
                    content=content,
                    start_line=start_line + 1,
                    end_line=end_line,
                    symbol_name=symbol_name,
                    chunk_type=chunk_type,
                )
        except Exception as e:
            logger.warning(f"Failed to extract node chunk: {e}")

        return None

    def _group_lines(
        self,
        lines: List[Tuple[int, str]],
        chunk_size: int,
    ) -> List[List[Tuple[int, str]]]:
        """Group lines into chunks of given size."""
        chunks = []
        current_chunk = []

        for idx, line in lines:
            current_chunk.append((idx, line))

            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk)
                # Overlap
                current_chunk = current_chunk[-self.OVERLAP :]

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def detect_language(self, filepath: str) -> str:
        """
        Detect programming language from file extension.

        Args:
            filepath: File path

        Returns:
            Language name or "unknown"
        """
        ext = filepath.lower().split(".")[-1] if "." in filepath else ""
        ext = "." + ext if ext else ""

        for lang, exts in self.LANGUAGE_EXTENSIONS.items():
            if ext in exts:
                return lang

        return "unknown"
