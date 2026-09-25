"""
Base Tool Interface for ReflexAgent
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class BaseTool(ABC):
    """
    Abstract base class for all tools available to the agent.
    """

    name: str = "base_tool"
    description: str = "Base tool description"
    is_destructive: bool = False  # If True, requires explicit System 1 safety clearance
    category: str = "general"

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool synchronously."""
        pass

    def get_routing_criteria(self) -> str:
        """Returns brief intent criteria for System 1 routing choice."""
        return self.description
