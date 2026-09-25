"""
Telemetry and Benchmarking Tracker for ReflexAgent
Quantifies latency reduction and dollar savings vs Pure LLM agents (OpenClaw, Hermes).
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from reflex_agent.core.schema import StepTrace


class TelemetrySummary(BaseModel):
    total_steps: int = 0
    system1_steps: int = 0
    system2_steps: int = 0
    system1_percentage: float = 0.0
    total_latency_ms: float = 0.0
    avg_latency_ms: float = 0.0
    agent_cost_usd: float = 0.0
    hypothetical_llm_cost_usd: float = 0.0
    dollars_saved_usd: float = 0.0
    savings_percentage: float = 0.0
    speedup_factor: float = 1.0
    security_attacks_blocked: int = 0


class TelemetryTracker:
    # Baseline LLM costs (e.g. GPT-4o / Claude 3.5 Sonnet / Hermes 70B via API)
    # Average LLM step cost: ~1000 input tokens + 200 output tokens = ~$0.005 to $0.01 per step
    # Average LLM step latency: ~1500ms - 3000ms
    LLM_COST_PER_STEP = 0.0075
    LLM_LATENCY_MS_PER_STEP = 2200.0

    def __init__(self):
        self.traces: List[StepTrace] = []
        self.attacks_blocked: int = 0
        self._start_time: float = time.time()

    def record_step(
        self,
        system_level: str,
        action: str,
        details: Dict[str, Any],
        latency_ms: float,
        confidence: float = 1.0,
        cost_usd: float = 0.0,
    ) -> StepTrace:
        step = StepTrace(
            step_number=len(self.traces) + 1,
            system_level=system_level,
            action=action,
            details=details,
            latency_ms=latency_ms,
            confidence=confidence,
            cost_usd=cost_usd,
        )
        self.traces.append(step)
        return step

    def record_attack_blocked(self):
        self.attacks_blocked += 1

    def get_summary(self) -> TelemetrySummary:
        total = len(self.traces)
        if total == 0:
            return TelemetrySummary()

        s1_steps = sum(1 for t in self.traces if "System 1" in t.system_level)
        s2_steps = sum(1 for t in self.traces if "System 2" in t.system_level)
        total_latency = sum(t.latency_ms for t in self.traces)
        avg_latency = total_latency / total if total > 0 else 0.0

        actual_cost = sum(t.cost_usd for t in self.traces)
        hypothetical_llm_cost = total * self.LLM_COST_PER_STEP
        saved_usd = max(0.0, hypothetical_llm_cost - actual_cost)
        savings_pct = (saved_usd / hypothetical_llm_cost * 100.0) if hypothetical_llm_cost > 0 else 0.0

        hypothetical_llm_latency = total * self.LLM_LATENCY_MS_PER_STEP
        speedup = (hypothetical_llm_latency / total_latency) if total_latency > 0 else 1.0

        return TelemetrySummary(
            total_steps=total,
            system1_steps=s1_steps,
            system2_steps=s2_steps,
            system1_percentage=round((s1_steps / total) * 100.0, 1),
            total_latency_ms=round(total_latency, 2),
            avg_latency_ms=round(avg_latency, 2),
            agent_cost_usd=round(actual_cost, 6),
            hypothetical_llm_cost_usd=round(hypothetical_llm_cost, 6),
            dollars_saved_usd=round(saved_usd, 6),
            savings_percentage=round(savings_pct, 1),
            speedup_factor=round(speedup, 1),
            security_attacks_blocked=self.attacks_blocked,
        )

    def reset(self):
        self.traces.clear()
        self.attacks_blocked = 0
        self._start_time = time.time()
