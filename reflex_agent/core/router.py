"""
Unified Reflex Router for System 1 Decisions
Seamlessly routes across Local Laya, TypeSafe Jev Cloud, and Fast Reflex Heuristic.
"""

from __future__ import annotations
import os
import time
import logging
from typing import Dict, Any, Union, List, Optional
from reflex_agent.core.schema import (
    Question,
    NoulQuestion,
    ChoiceQuestion,
    ScoreQuestion,
    Decision,
    ReflexDecisionResult,
    QuestionType,
    ProviderType,
)

logger = logging.getLogger("reflex_agent.router")


class ReflexRouter:
    """
    Unified System 1 decision router.
    Orchestrates local Laya, TypeSafe Jev API, and fast fallback.
    """

    def __init__(
        self,
        provider: Union[str, ProviderType] = ProviderType.AUTO,
        model: str = "english",
        device: Optional[str] = None,
        typesafe_api_key: Optional[str] = None,
        kev_base_url: Optional[str] = None,
        preload_laya: bool = True,
    ):
        if isinstance(provider, str):
            provider = ProviderType(provider.lower())
        self.requested_provider = provider
        self.model_name = model
        self.device = device or "cpu"
        self.typesafe_api_key = typesafe_api_key or os.environ.get("TYPESAFE_API_KEY")
        self.kev_base_url = kev_base_url or os.environ.get("KEV_BASE_URL")
        self.preload_laya = preload_laya

        self._laya_router = None
        self._typesafe_client = None
        self._kev_client = None
        self.active_provider: str = "uninitialized"

        self._initialize_provider()

    def _initialize_provider(self):
        # 1. Try Kev (Jared Palmer's open-weights Qwen-based System 1) if requested or base_url given
        if (self.requested_provider == ProviderType.KEV or (self.requested_provider == ProviderType.AUTO and self.kev_base_url)):
            try:
                from typesafe_sdk import TypeSafeClient
                base_url = self.kev_base_url or "http://127.0.0.1:8009"
                self._kev_client = TypeSafeClient(api_key="local", base_url=base_url)
                self.active_provider = "kev"
                logger.info(f"ReflexRouter initialized with Kev endpoint ({base_url})")
                return
            except Exception as e:
                logger.warning(f"Failed to connect to Kev endpoint: {e}")

        # 2. Try Jev if explicitly requested or key available
        if self.requested_provider in (ProviderType.JEV, ProviderType.AUTO) and self.typesafe_api_key:
            try:
                from typesafe_sdk import TypeSafeClient
                self._typesafe_client = TypeSafeClient(api_key=self.typesafe_api_key)
                self.active_provider = "jev"
                logger.info("ReflexRouter initialized with TypeSafe Jev Cloud API")
                return
            except Exception as e:
                logger.warning(f"Failed to initialize TypeSafe Jev client: {e}")

        # 3. Try Laya if explicitly requested or auto
        if self.requested_provider in (ProviderType.LAYA, ProviderType.AUTO):
            try:
                import laya
                self._laya_router = laya.Router(
                    default=self.model_name,
                    device=self.device,
                    preload=self.preload_laya,
                )
                self.active_provider = "laya"
                logger.info(f"ReflexRouter initialized with local Laya ({self.model_name})")
                return
            except Exception as e:
                logger.warning(f"Local Laya initialization skipped: {e}")

        # 4. Fallback to fast semantic heuristic engine
        self.active_provider = "fast_reflex_heuristic"
        logger.info("ReflexRouter initialized with Fast Reflex Heuristic engine (sub-10ms fallback)")

    def decide(
        self,
        state: Union[str, Dict[str, Any], List[Any]],
        questions: Dict[str, Question],
    ) -> ReflexDecisionResult:
        """
        Evaluate non-autoregressive typed decisions against state.
        Returns strict typed values (choice, noul, score) with confidence scores.
        """
        start_time = time.perf_counter()

        # Route through active provider
        if self.active_provider == "kev" and self._kev_client is not None:
            try:
                return self._predict_jev(state, questions, start_time, client=self._kev_client, provider_label="kev-self-hosted")
            except Exception as e:
                logger.warning(f"Kev endpoint call failed, falling back: {e}")

        if self.active_provider == "laya" and self._laya_router is not None:
            try:
                result = self._predict_laya(state, questions, start_time)
                return result
            except Exception as e:
                logger.warning(f"Laya predict failed, falling back: {e}")

        if self.active_provider == "jev" and self._typesafe_client is not None:
            try:
                result = self._predict_jev(state, questions, start_time)
                return result
            except Exception as e:
                logger.warning(f"TypeSafe Jev API call failed, falling back: {e}")

        # Fallback heuristic
        return self._predict_heuristic(state, questions, start_time)

    def _predict_laya(
        self,
        state: Union[str, Dict[str, Any], List[Any]],
        questions: Dict[str, Question],
        start_time: float,
    ) -> ReflexDecisionResult:
        """Execute via local Laya modernBERT router."""
        laya_questions = {}
        for q_name, q in questions.items():
            if isinstance(q, NoulQuestion):
                laya_questions[q_name] = {"type": "noul", "instructions": q.instructions}
                if q.criteria:
                    laya_questions[q_name]["criteria"] = q.criteria
            elif isinstance(q, ChoiceQuestion):
                laya_questions[q_name] = {"type": "choice", "instructions": q.instructions, "criteria": q.criteria}
            elif isinstance(q, ScoreQuestion):
                laya_questions[q_name] = {"type": "score", "instructions": q.instructions, "criteria": q.criteria}

        raw_result = self._laya_router.predict(state=state, questions=laya_questions)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        decisions = {}
        # Parse laya decisions from raw_result['answers']
        answers_dict = {}
        if isinstance(raw_result, dict):
            answers_dict = raw_result.get("answers", raw_result)
        elif hasattr(raw_result, "answers") and isinstance(raw_result.answers, dict):
            answers_dict = raw_result.answers

        for k, v in answers_dict.items():
            q_def = questions.get(k)
            q_type = q_def.type if q_def else QuestionType.CHOICE
            
            val = None
            conf = 0.95
            probs = None

            if isinstance(v, dict):
                val = v.get("choice") if "choice" in v else (v.get("noul") if "noul" in v else v.get("score", v.get("value")))
                conf = v.get("confidence") or v.get("answer_confidence", 0.95)
                probs = v.get("probabilities")
            elif hasattr(v, "choice"):
                val = v.choice
                conf = getattr(v, "confidence", 0.95)
                probs = getattr(v, "probabilities", None)
            elif hasattr(v, "noul"):
                val = v.noul
                conf = getattr(v, "confidence", 0.95)
                probs = getattr(v, "probabilities", None)
            elif hasattr(v, "score"):
                val = v.score
                conf = getattr(v, "confidence", 0.95)
                probs = getattr(v, "probabilities", None)
            else:
                val = v

            decisions[k] = Decision(
                name=k,
                type=q_type,
                value=val if val is not None else False,
                confidence=float(conf) if conf is not None else 0.95,
                probabilities=probs,
                raw_response=v,
            )

        return ReflexDecisionResult(
            state=state,
            decisions=decisions,
            latency_ms=round(elapsed_ms, 2),
            provider="laya-local",
            model=self.model_name,
            tokens_used=0,
            estimated_cost_usd=0.0,
        )

    def _predict_jev(
        self,
        state: Union[str, Dict[str, Any], List[Any]],
        questions: Dict[str, Question],
        start_time: float,
        client: Optional[Any] = None,
        provider_label: str = "jev-cloud",
    ) -> ReflexDecisionResult:
        """Execute via TypeSafe Jev API or self-hosted Kev endpoint."""
        from typesafe_sdk import Choice, Noul, Score

        target_client = client or self._typesafe_client
        if target_client is None:
            raise RuntimeError("No TypeSafe/Kev client initialized")

        jev_questions = {}
        for q_name, q in questions.items():
            if isinstance(q, NoulQuestion):
                jev_questions[q_name] = Noul(instructions=q.instructions, criteria=q.criteria)
            elif isinstance(q, ChoiceQuestion):
                jev_questions[q_name] = Choice(instructions=q.instructions, criteria=q.criteria)
            elif isinstance(q, ScoreQuestion):
                jev_questions[q_name] = Score(instructions=q.instructions, criteria=q.criteria)

        response = target_client.system_one(state=state, questions=jev_questions)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        decisions = {}
        for q_name, ans in response.answers.items():
            q_def = questions.get(q_name)
            q_type = q_def.type if q_def else QuestionType.CHOICE

            if hasattr(ans, "choice"):
                val = ans.choice
            elif hasattr(ans, "noul"):
                val = ans.noul
            elif hasattr(ans, "score"):
                val = ans.score
            else:
                val = getattr(ans, "value", None)

            conf = getattr(ans, "confidence", 0.98)
            probs = getattr(ans, "probabilities", None)

            decisions[q_name] = Decision(
                name=q_name,
                type=q_type,
                value=val,
                confidence=float(conf) if conf is not None else 0.98,
                probabilities=probs,
                raw_response=ans,
            )

        tokens = getattr(response.usage, "input_tokens", 50) if hasattr(response, "usage") else 50
        cost = tokens * (42.0 / 1_000_000_000.0) if provider_label == "jev-cloud" else 0.0

        return ReflexDecisionResult(
            state=state,
            decisions=decisions,
            latency_ms=round(elapsed_ms, 2),
            provider=provider_label,
            model="kev-latest" if "kev" in provider_label else "jev-1.13",
            tokens_used=tokens,
            estimated_cost_usd=round(cost, 8),
        )

    def _predict_heuristic(
        self,
        state: Union[str, Dict[str, Any], List[Any]],
        questions: Dict[str, Question],
        start_time: float,
    ) -> ReflexDecisionResult:
        """
        Fast semantic heuristic matcher.
        Serves as an ultra-fast sub-2ms fallback for testing and edge runtime.
        """
        if isinstance(state, dict):
            state_str = " ".join(str(v) for v in state.values()).lower()
        elif isinstance(state, list):
            state_str = " ".join(str(v) for v in state).lower()
        else:
            state_str = str(state).lower()

        decisions = {}

        for q_name, q in questions.items():
            if isinstance(q, NoulQuestion):
                # Precise safety classifications
                if q_name in ("jailbreak", "prompt_injection"):
                    injection_triggers = (
                        "ignore previous instructions", "system prompt", "override instructions",
                        "pretend you are unrestricted", "dan mode", "disregard safety",
                        "bypass guardrails", "jailbreak", "dump database"
                    )
                    matched = any(t in state_str for t in injection_triggers)
                elif q_name == "sensitive_data":
                    sensitive_triggers = (
                        "password", "api_key", "secret_key", "bearer ey", "private_key",
                        "aws_secret", "id_rsa", "session_token"
                    )
                    matched = any(t in state_str for t in sensitive_triggers)
                elif q_name == "destructive_action":
                    destructive_triggers = (
                        "rm -rf", "format c:", "format disk", "drop table", "drop database",
                        "delete from users", "truncate table", "unlink /", "kill -9 1", "shutdown /s"
                    )
                    matched = any(t in state_str for t in destructive_triggers)
                elif q_name == "requires_tools":
                    tool_indicators = (
                        "calculate", "compute", "*", "/", "+", "-", "math",
                        "mandi", "bhav", "price", "rate", "भाव", "दाम", "मंडी",
                        "crop", "soil", "npk", "fertilizer", "खाद", "मिट्टी", "फसल",
                        "leaf", "disease", "पत्ती", "रोग", "panchayat", "weather",
                        "file", "read", "write", "search", "run command"
                    )
                    matched = any(t in state_str for t in tool_indicators)
                else:
                    instr_words = [w.strip("?,.`'\"") for w in q.instructions.lower().split() if len(w) > 4]
                    matched = any(w in state_str for w in instr_words)

                decisions[q_name] = Decision(
                    name=q_name,
                    type=QuestionType.NOUL,
                    value=matched,
                    confidence=0.95 if matched else 0.90,
                )

            elif isinstance(q, ChoiceQuestion):
                best_choice = None
                best_score = -1

                import re
                state_tokens = set(re.findall(r"\w+", state_str))

                for opt_key, opt_desc in q.criteria.items():
                    key_tokens = set(re.findall(r"\w+", opt_key.lower()))
                    desc_tokens = set(re.findall(r"\w+", opt_desc.lower())) if opt_desc else set()

                    key_overlap = len(state_tokens & key_tokens)
                    desc_overlap = len(state_tokens & desc_tokens)

                    all_target_tokens = key_tokens | desc_tokens
                    stem_overlap = sum(
                        1 for st in state_tokens
                        if len(st) >= 3 and any(
                            (st.startswith(dt[:4]) or dt.startswith(st[:4]) or st in dt or dt in st)
                            for dt in all_target_tokens if len(dt) >= 3
                        )
                    )

                    score = (key_overlap * 6) + (desc_overlap * 4) + (stem_overlap * 3)
                    if score > best_score:
                        best_score = score
                        best_choice = opt_key

                if not best_choice or best_score == 0:
                    best_choice = list(q.criteria.keys())[-1]

                decisions[q_name] = Decision(
                    name=q_name,
                    type=QuestionType.CHOICE,
                    value=best_choice,
                    confidence=0.92 if best_score > 0 else 0.75,
                )

            elif isinstance(q, ScoreQuestion):
                score_val = 0
                for idx, crit in enumerate(q.criteria):
                    crit_lower = crit.lower()
                    if "severe" in crit_lower and any(w in state_str for w in ["kill", "malware", "weapon", "terror", "ransomware"]):
                        score_val = max(score_val, idx)
                    elif "serious" in crit_lower and any(w in state_str for w in ["exploit", "hack", "dump", "steal"]):
                        score_val = max(score_val, idx)
                    elif "minor" in crit_lower and any(w in state_str for w in ["curse", "bypass"]):
                        score_val = max(score_val, idx)

                decisions[q_name] = Decision(
                    name=q_name,
                    type=QuestionType.SCORE,
                    value=score_val,
                    confidence=0.90,
                )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ReflexDecisionResult(
            state=state,
            decisions=decisions,
            latency_ms=round(elapsed_ms, 2),
            provider="reflex-fast-engine",
            model="reflex-v1",
            tokens_used=0,
            estimated_cost_usd=0.0,
        )
