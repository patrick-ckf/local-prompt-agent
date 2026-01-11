# -*- coding: utf-8 -*-
"""
File operations tool.

Safe file reading with restrictions.
"""

from pathlib import Path
from typing import Any, Dict

from local_prompt_agent.tools.base import Tool


class FileReadTool(Tool):
    """
    Read file contents.

    Restricted to safe directories for security.
    """

    def __init__(self, allowed_paths: list[str] | None = None):
        """
        Initialize file read tool.

        Args:
            allowed_paths: List of allowed directory paths (optional)
        """
        super().__init__(
            name="read_file",
            description="Read the contents of a text file. "
            "Returns the file content as a string.",
        )
        self.allowed_paths = [Path(p) for p in (allowed_paths or ["."])]

    def get_parameters(self) -> Dict[str, Any]:
        """Get parameter schema."""
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read",
                }
            },
            "required": ["file_path"],
        }

    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Read file contents.

        Args:
            file_path: Path to file

        Returns:
            File contents or error
        """
        file_path_str = kwargs.get("file_path", "")

        if not file_path_str:
            return {"success": False, "error": "file_path is required"}

        try:
            file_path = Path(file_path_str)

            # Security: check if path is allowed
            if not self._is_allowed_path(file_path):
                return {
                    "success": False,
                    "error": "Access denied: Path not in allowed directories",
                }

            # Check if file exists
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                }

            # Check if it's a file
            if not file_path.is_file():
                return {
                    "success": False,
                    "error": f"Not a file: {file_path}",
                }

            # Read file with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return {
                "success": True,
                "file_path": str(file_path),
                "content": content,
                "size": len(content),
            }

        except UnicodeDecodeError:
            return {
                "success": False,
                "error": "File is not a text file or has encoding issues",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading file: {str(e)}",
            }

    def _is_allowed_path(self, path: Path) -> bool:
        """
        Check if path is in allowed directories.

        Args:
            path: Path to check

        Returns:
            True if allowed
        """
        try:
            # Resolve to absolute path
            absolute_path = path.resolve()

            # Check against allowed paths
            for allowed in self.allowed_paths:
                allowed_absolute = allowed.resolve()
                try:
                    # Check if path is within allowed directory
                    absolute_path.relative_to(allowed_absolute)
                    return True
                except ValueError:
                    continue

            return False

        except Exception:
            return False
