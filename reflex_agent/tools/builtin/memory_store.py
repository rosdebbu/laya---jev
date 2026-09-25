"""
Reflex Memory Store Tool
Fast key-value cache and persistent facts memory.
"""

from __future__ import annotations
import time
from typing import Dict, Any, Optional
from reflex_agent.tools.base import BaseTool, ToolResult


class MemoryStoreTool(BaseTool):
    name: str = "memory_store"
    description: str = "Store, retrieve, or update user facts, session parameters, and long-term memory"
    is_destructive: bool = False
    category: str = "memory"

    def __init__(self):
        self._store: Dict[str, Any] = {}

    def execute(self, action: str, key: str, value: Optional[Any] = None, **kwargs) -> ToolResult:
        start = time.perf_counter()
        action = action.lower()

        if action == "get":
            val = self._store.get(key)
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=(val is not None),
                output=val,
                error=None if val is not None else f"Key '{key}' not found in memory",
                execution_time_ms=round(elapsed, 2)
            )

        elif action == "set":
            self._store[key] = value
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=True,
                output=f"Stored '{key}' = {value}",
                execution_time_ms=round(elapsed, 2)
            )

        elif action == "delete":
            removed = self._store.pop(key, None)
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=True,
                output=f"Deleted '{key}' (was: {removed})",
                execution_time_ms=round(elapsed, 2)
            )

        elif action == "list_all":
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=True,
                output=dict(self._store),
                execution_time_ms=round(elapsed, 2)
            )

        else:
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=False,
                output=None,
                error=f"Unsupported memory action: {action}",
                execution_time_ms=round(elapsed, 2)
            )
