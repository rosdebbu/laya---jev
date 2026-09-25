"""
ReflexAgent State Management
Maintains conversation memory, tool results, and reflex context.
"""

from __future__ import annotations
import uuid
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolCallRecord(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    output: Any
    is_success: bool = True
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0


class AgentState(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = Field(default_factory=list)
    memory_store: Dict[str, Any] = Field(default_factory=dict)
    tool_history: List[ToolCallRecord] = Field(default_factory=list)
    current_intent: Optional[str] = None
    detected_language: str = "english"
    iteration_count: int = 0
    is_terminated: bool = False
    final_response: Optional[str] = None

    def add_user_message(self, content: str) -> Message:
        msg = Message(role="user", content=content)
        self.messages.append(msg)
        return msg

    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Message:
        msg = Message(role="assistant", content=content, metadata=metadata or {})
        self.messages.append(msg)
        return msg

    def add_tool_record(self, record: ToolCallRecord):
        self.tool_history.append(record)

    def to_reflex_context(self) -> Dict[str, Any]:
        """Convert current state into high-signal representation for System 1."""
        last_user = next((m.content for m in reversed(self.messages) if m.role == "user"), "")
        recent_tools = [r.tool_name for r in self.tool_history[-3:]]
        return {
            "last_user_message": last_user,
            "recent_tools": recent_tools,
            "current_intent": self.current_intent,
            "iteration": self.iteration_count,
        }
