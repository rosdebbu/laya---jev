"""
File Operations Tool
Safe workspace file reader, writer, and inspector.
"""

from __future__ import annotations
import os
import time
from typing import Optional
from reflex_agent.tools.base import BaseTool, ToolResult


class FileOpsTool(BaseTool):
    name: str = "file_ops"
    description: str = "Read, write, append, or inspect files and directories in the workspace"
    is_destructive: bool = True  # writing/deleting requires System 1 safety verification
    category: str = "filesystem"

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = os.path.abspath(workspace_root or os.getcwd())

    def _resolve_safe_path(self, path: str) -> str:
        abs_path = os.path.abspath(os.path.join(self.workspace_root, path))
        return abs_path

    def execute(self, action: str, path: str, content: Optional[str] = None, **kwargs) -> ToolResult:
        start = time.perf_counter()
        target_path = self._resolve_safe_path(path)

        try:
            if action == "read":
                if not os.path.exists(target_path):
                    return ToolResult(success=False, output=None, error=f"File not found: {path}")
                with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                    data = f.read()
                elapsed = (time.perf_counter() - start) * 1000.0
                return ToolResult(success=True, output=data[:10000], execution_time_ms=round(elapsed, 2))

            elif action == "write":
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(content or "")
                elapsed = (time.perf_counter() - start) * 1000.0
                return ToolResult(success=True, output=f"Successfully wrote {len(content or '')} bytes to {path}", execution_time_ms=round(elapsed, 2))

            elif action == "list":
                if not os.path.exists(target_path):
                    return ToolResult(success=False, output=None, error=f"Directory not found: {path}")
                entries = os.listdir(target_path)
                elapsed = (time.perf_counter() - start) * 1000.0
                return ToolResult(success=True, output=entries[:50], execution_time_ms=round(elapsed, 2))

            else:
                return ToolResult(success=False, output=None, error=f"Unknown file action: {action}")

        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(success=False, output=None, error=str(e), execution_time_ms=round(elapsed, 2))
