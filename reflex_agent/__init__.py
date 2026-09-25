"""
ReflexAgent: Sub-50ms Type-Safe Dual-Brain AI Agent Framework
Powered by Laya (System 1 Local) + Jev (System 1 Cloud) + LiteLLM (System 2 Reasoning)
"""

from reflex_agent.core.schema import (
    NoulQuestion,
    ChoiceQuestion,
    ScoreQuestion,
    Decision,
    ReflexDecisionResult,
    AgentMode,
)
from reflex_agent.core.router import ReflexRouter
from reflex_agent.core.guardrails import ReflexGuardrail
from reflex_agent.core.telemetry import TelemetryTracker
from reflex_agent.core.engine import DualBrainAgent
from reflex_agent.core.state import AgentState, Message

__version__ = "0.1.0"

__all__ = [
    "DualBrainAgent",
    "ReflexRouter",
    "ReflexGuardrail",
    "TelemetryTracker",
    "AgentState",
    "Message",
    "NoulQuestion",
    "ChoiceQuestion",
    "ScoreQuestion",
    "Decision",
    "ReflexDecisionResult",
    "AgentMode",
]
