"""
Unit tests for ReflexAgent Schemas
"""

import pytest
from reflex_agent.core.schema import (
    NoulQuestion,
    ChoiceQuestion,
    ScoreQuestion,
    QuestionType,
    Decision,
    ReflexDecisionResult,
)


def test_question_schemas():
    noul = NoulQuestion(instructions="Is this safe?")
    assert noul.type == QuestionType.NOUL

    choice = ChoiceQuestion(
        instructions="Pick category",
        criteria={"a": "option a", "b": "option b"},
    )
    assert choice.type == QuestionType.CHOICE
    assert "a" in choice.criteria

    score = ScoreQuestion(
        instructions="Rank urgency",
        criteria=["low", "medium", "high"],
    )
    assert score.type == QuestionType.SCORE
    assert len(score.criteria) == 3


def test_decision_result_parsing():
    decisions = {
        "is_refund": Decision(name="is_refund", type=QuestionType.NOUL, value=True, confidence=0.92),
        "team": Decision(name="team", type=QuestionType.CHOICE, value="billing", confidence=0.88),
        "urgency": Decision(name="urgency", type=QuestionType.SCORE, value=2, confidence=0.85),
    }

    result = ReflexDecisionResult(
        state={"text": "sample"},
        decisions=decisions,
        latency_ms=12.5,
        provider="laya-local",
        model="english",
    )

    assert result.get_noul("is_refund") is True
    assert result.get_choice("team") == "billing"
    assert result.get_score("urgency") == 2
    assert result.get_confidence("team") == 0.88
