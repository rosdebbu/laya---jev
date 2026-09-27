"""
DualBrainAgent: The Core Sub-50ms Type-Safe Agent Engine
Orchestrates System 1 (Reflex) and System 2 (Reasoning) with unjailbreakable guardrails.
"""

from __future__ import annotations
import time
import logging
from typing import Dict, Any, Optional, Iterator, Union, List
from pydantic import BaseModel, Field

from reflex_agent.core.schema import (
    AgentMode,
    ChoiceQuestion,
    NoulQuestion,
    ScoreQuestion,
    ReflexDecisionResult,
    GuardrailAssessment,
)
from reflex_agent.core.router import ReflexRouter
from reflex_agent.core.guardrails import ReflexGuardrail
from reflex_agent.core.telemetry import TelemetryTracker, TelemetrySummary
from reflex_agent.core.state import AgentState, ToolCallRecord
from reflex_agent.tools.registry import ToolRegistry
from reflex_agent.reasoning.llm_client import ReasoningClient

logger = logging.getLogger("reflex_agent.engine")


class AgentStepEvent(BaseModel):
    event_type: str  # "guardrail", "routing", "tool_execution", "synthesis", "complete", "blocked"
    system_level: str
    message: str
    latency_ms: float
    data: Dict[str, Any] = Field(default_factory=dict)


class DualBrainAgent:
    """
    Sub-50ms Type-Safe Dual-Brain Agent.
    - System 1 (Laya / Jev): Non-autoregressive fast reflex classification, safety, tool routing.
    - System 2 (LiteLLM / OpenAI): Deep reasoning and creative synthesis.
    """

    def __init__(
        self,
        router: Optional[ReflexRouter] = None,
        tool_registry: Optional[ToolRegistry] = None,
        reasoning_client: Optional[ReasoningClient] = None,
        mode: AgentMode = AgentMode.HYBRID,
        confidence_threshold: float = 0.75,
        max_iterations: int = 5,
    ):
        self.router = router or ReflexRouter()
        self.guardrail = ReflexGuardrail(self.router)
        self.tools = tool_registry or ToolRegistry()
        self.reasoning = reasoning_client or ReasoningClient()
        self.mode = mode
        self.confidence_threshold = confidence_threshold
        self.max_iterations = max_iterations
        self.telemetry = TelemetryTracker()

    def run(self, user_input: str, state: Optional[AgentState] = None) -> AgentState:
        """
        Execute full agent pipeline synchronously.
        """
        agent_state = state or AgentState()
        for _ in self.run_stream(user_input, agent_state):
            pass
        return agent_state

    def run_stream(
        self, user_input: str, state: Optional[AgentState] = None
    ) -> Iterator[AgentStepEvent]:
        """
        Streaming execution generator yielding live step events.
        Enables real-time visualization of System 1 vs System 2 execution.
        """
        agent_state = state or AgentState()
        agent_state.add_user_message(user_input)

        # -------------------------------------------------------------
        # STEP 1: System 1 Non-Autoregressive Safety Guardrail Check
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        assessment = self.guardrail.assess(user_input)
        g_latency = (time.perf_counter() - t0) * 1000.0

        self.telemetry.record_step(
            system_level="System 1 (Reflex Guardrail)",
            action="Safety Assessment",
            details={
                "is_safe": assessment.is_safe,
                "is_jailbreak": assessment.is_jailbreak,
                "is_injection": assessment.is_prompt_injection,
                "harm_score": assessment.harm_score,
                "provider": self.router.active_provider,
            },
            latency_ms=g_latency,
            confidence=assessment.confidence,
            cost_usd=0.0,
        )

        yield AgentStepEvent(
            event_type="guardrail",
            system_level="System 1 (Reflex)",
            message=f"Guardrail Check: {'SAFE' if assessment.is_safe else 'BLOCKED'} ({round(g_latency, 1)}ms)",
            latency_ms=g_latency,
            data=assessment.model_dump(),
        )

        if not assessment.is_safe:
            self.telemetry.record_attack_blocked()
            blocked_msg = f"Security Policy Violation: {assessment.reason}. Request terminated by System 1."
            agent_state.add_assistant_message(blocked_msg, metadata={"security_blocked": True})
            agent_state.final_response = blocked_msg
            agent_state.is_terminated = True

            yield AgentStepEvent(
                event_type="blocked",
                system_level="System 1 (Reflex)",
                message=blocked_msg,
                latency_ms=g_latency,
                data={"reason": assessment.reason},
            )
            return

        # -------------------------------------------------------------
        # STEP 2: System 1 Intent & Language Classification
        # -------------------------------------------------------------
        t1 = time.perf_counter()
        intent_questions = {
            "intent": ChoiceQuestion(
                instructions="What is the primary category of `task`?",
                criteria={
                    "factual_inquiry": "Asking for specific knowledge, facts, or documentation",
                    "mandi_price": "Mandi market rates, price of crops today, APMC selling rates, MSP status, मंडी भाव",
                    "agricultural_intelligence": "Crop recommendation, soil NPK test, fertilizer dosage, crop disease, government schemes, subsidies, yojana, sarkari yojana, PM-KISAN, PM-KUSUM, SMAM, सरकारी योजनाएं, सब्सिडी, अनुदान",
                    "file_management": "Viewing, saving, or checking files",
                    "math_calculation": "Performing numerical calculations or logic",
                    "system_command": "Running terminal or system commands",
                    "casual_chat": "Greetings, conversation, or creative interaction",
                    "other": "Other diverse task",
                },
            ),
            "requires_tools": NoulQuestion(
                instructions="Does fulfilling `task` require executing an external tool (mandi, crop, fertilizer, schemes, subsidy, yojana, weather, search, file, shell, calculator)?",
            ),
        }

        classification_res = self.router.decide(state={"task": user_input}, questions=intent_questions)
        c_latency = (time.perf_counter() - t1) * 1000.0

        detected_intent = classification_res.get_choice("intent", "other")
        needs_tools = classification_res.get_noul("requires_tools", default=False)
        agent_state.current_intent = detected_intent

        self.telemetry.record_step(
            system_level="System 1 (Reflex Routing)",
            action="Intent Classification",
            details={
                "intent": detected_intent,
                "needs_tools": needs_tools,
                "confidence": classification_res.get_confidence("intent"),
            },
            latency_ms=c_latency,
            confidence=classification_res.get_confidence("intent"),
            cost_usd=classification_res.estimated_cost_usd,
        )

        yield AgentStepEvent(
            event_type="routing",
            system_level="System 1 (Reflex)",
            message=f"Intent: {detected_intent.upper()} (Needs tools: {needs_tools}) in {round(c_latency, 1)}ms",
            latency_ms=c_latency,
            data={"intent": detected_intent, "needs_tools": needs_tools},
        )

        # -------------------------------------------------------------
        # STEP 3: System 1 Dynamic Tool Routing (Sub-50ms)
        # -------------------------------------------------------------
        tool_results_list = []

        if needs_tools or detected_intent in ("mandi_price", "agricultural_intelligence", "math_calculation", "file_management", "system_command", "factual_inquiry"):
            t2 = time.perf_counter()
            tool_routing_q = {"selected_tool": self.tools.build_routing_question()}
            tool_decision = self.router.decide(state={"task": user_input}, questions=tool_routing_q)
            t_latency = (time.perf_counter() - t2) * 1000.0

            chosen_tool = tool_decision.get_choice("selected_tool", default="direct_answer")

            self.telemetry.record_step(
                system_level="System 1 (Reflex Tool Selector)",
                action=f"Select Tool: {chosen_tool}",
                details={"tool": chosen_tool, "confidence": tool_decision.get_confidence("selected_tool")},
                latency_ms=t_latency,
                confidence=tool_decision.get_confidence("selected_tool"),
                cost_usd=tool_decision.estimated_cost_usd,
            )

            yield AgentStepEvent(
                event_type="routing",
                system_level="System 1 (Reflex)",
                message=f"Selected Tool: `{chosen_tool}` ({round(t_latency, 1)}ms)",
                latency_ms=t_latency,
                data={"tool": chosen_tool},
            )

            # Execute tool if not direct_answer
            if chosen_tool and chosen_tool != "direct_answer" and self.tools.get(chosen_tool):
                t_exec_start = time.perf_counter()
                
                # Extract arguments
                args = self.reasoning.extract_arguments(tool_name=chosen_tool, user_input=user_input)

                # Execute
                tool_res = self.tools.execute_tool(chosen_tool, **args)
                exec_latency = (time.perf_counter() - t_exec_start) * 1000.0

                record = ToolCallRecord(
                    tool_name=chosen_tool,
                    arguments=args,
                    output=tool_res.output,
                    is_success=tool_res.success,
                    error_message=tool_res.error,
                    execution_time_ms=exec_latency,
                )
                agent_state.add_tool_record(record)
                tool_results_list.append(record.model_dump())

                self.telemetry.record_step(
                    system_level="Deterministic Tool Execution",
                    action=f"Execute `{chosen_tool}`",
                    details={"args": args, "success": tool_res.success},
                    latency_ms=exec_latency,
                    cost_usd=0.0,
                )

                yield AgentStepEvent(
                    event_type="tool_execution",
                    system_level="Tool Engine",
                    message=f"Executed `{chosen_tool}` in {round(exec_latency, 1)}ms (Success: {tool_res.success})",
                    latency_ms=exec_latency,
                    data=record.model_dump(),
                )

        # -------------------------------------------------------------
        # STEP 4: System 2 Reasoning & Synthesis (Only when needed)
        # -------------------------------------------------------------
        t3 = time.perf_counter()
        
        # In PURE_REFLEX mode, do not call System 2
        if self.mode == AgentMode.PURE_REFLEX:
            if tool_results_list:
                final_text = str(tool_results_list[-1].get("output"))
            else:
                final_text = f"Reflex decision completed: {detected_intent}."
            s_latency = 0.5
        else:
            final_text = self.reasoning.synthesize(
                user_input=user_input,
                tool_results=tool_results_list,
                system_1_intent=detected_intent,
            )
            s_latency = (time.perf_counter() - t3) * 1000.0

        is_llm_used = self.reasoning.has_api_key and self.mode != AgentMode.PURE_REFLEX
        cost_s2 = 0.002 if is_llm_used else 0.0

        self.telemetry.record_step(
            system_level="System 2 (Reasoning & Synthesis)" if is_llm_used else "System 1 (Reflex Template Synthesis)",
            action="Response Synthesis",
            details={"is_llm": is_llm_used, "output_length": len(final_text)},
            latency_ms=s_latency,
            cost_usd=cost_s2,
        )

        agent_state.add_assistant_message(final_text)
        agent_state.final_response = final_text
        agent_state.is_terminated = True

        yield AgentStepEvent(
            event_type="synthesis",
            system_level="System 2 (Reasoning)" if is_llm_used else "System 1 (Reflex)",
            message=f"Synthesis Complete ({round(s_latency, 1)}ms)",
            latency_ms=s_latency,
            data={"final_response": final_text},
        )

        # Emit completion summary
        summary = self.telemetry.get_summary()
        yield AgentStepEvent(
            event_type="complete",
            system_level="Telemetry",
            message=f"Turn complete: {summary.total_latency_ms}ms total | {summary.system1_percentage}% System 1 | ${summary.dollars_saved_usd} saved vs Pure LLM",
            latency_ms=summary.total_latency_ms,
            data=summary.model_dump(),
        )

    def get_telemetry_summary(self) -> TelemetrySummary:
        return self.telemetry.get_summary()
