"""
ReflexAgent Type-Safe Schema Definitions
Compatible with Laya (local) and TypeSafe Jev (cloud) System 1 specifications.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    NOUL = "noul"
    CHOICE = "choice"
    SCORE = "score"


class AgentMode(str, Enum):
    PURE_REFLEX = "pure_reflex"       # Only System 1 (33ms, 0 LLM cost)
    HYBRID = "hybrid"                 # System 1 reflex + System 2 LLM when needed (Recommended)
    PURE_LLM = "pure_llm"             # OpenClaw / Hermes baseline (all LLM steps)


class ProviderType(str, Enum):
    AUTO = "auto"
    LAYA = "laya"
    KEV = "kev"
    JEV = "jev"
    MOCK = "mock"


class BaseQuestion(BaseModel):
    instructions: str = Field(..., description="Prompt/instruction defining what to evaluate")


class NoulQuestion(BaseQuestion):
    type: QuestionType = QuestionType.NOUL
    criteria: Optional[List[str]] = Field(default=None, description="Optional custom boolean labels")


class ChoiceQuestion(BaseQuestion):
    type: QuestionType = QuestionType.CHOICE
    criteria: Dict[str, Optional[str]] = Field(..., description="Map of candidate keys to their description")


class ScoreQuestion(BaseQuestion):
    type: QuestionType = QuestionType.SCORE
    criteria: List[str] = Field(..., description="Ordered list of criteria from lowest to highest score")


Question = Union[NoulQuestion, ChoiceQuestion, ScoreQuestion]


class Decision(BaseModel):
    name: str
    type: QuestionType
    value: Union[bool, str, int, float]
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    probabilities: Optional[Dict[str, float]] = None
    raw_response: Optional[Any] = None

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.70


class ReflexDecisionResult(BaseModel):
    state: Union[str, Dict[str, Any], List[Any]]
    decisions: Dict[str, Decision]
    latency_ms: float
    provider: str
    model: str
    tokens_used: int = 0
    estimated_cost_usd: float = 0.0

    def get_choice(self, question_name: str, default: Optional[str] = None) -> Optional[str]:
        d = self.decisions.get(question_name)
        if d and d.type == QuestionType.CHOICE:
            return str(d.value)
        return default

    def get_noul(self, question_name: str, default: bool = False) -> bool:
        d = self.decisions.get(question_name)
        if d and d.type == QuestionType.NOUL:
            if isinstance(d.value, float):
                return d.value >= 0.5
            return bool(d.value)
        return default

    def get_score(self, question_name: str, default: int = 0) -> int:
        d = self.decisions.get(question_name)
        if d and d.type == QuestionType.SCORE:
            return int(d.value)
        return default

    def get_confidence(self, question_name: str) -> float:
        d = self.decisions.get(question_name)
        return d.confidence if d else 0.0


class GuardrailAssessment(BaseModel):
    is_safe: bool = True
    is_jailbreak: bool = False
    is_prompt_injection: bool = False
    contains_sensitive_data: bool = False
    harm_score: int = 0
    harm_level: str = "none"
    confidence: float = 1.0
    latency_ms: float = 0.0
    reason: Optional[str] = None


class StepTrace(BaseModel):
    step_number: int
    system_level: str  # "System 1 (Reflex)" or "System 2 (Reasoning)"
    action: str
    details: Dict[str, Any]
    latency_ms: float
    confidence: float
    cost_usd: float
