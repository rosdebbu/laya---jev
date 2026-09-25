"""
Precision Calculator Tool
Solves mathematical, financial, and statistical queries deterministically.
Compensates for the known limit of System 1 on raw calculation.
"""

from __future__ import annotations
import math
import time
from typing import Any
from reflex_agent.tools.base import BaseTool, ToolResult


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Perform math arithmetic, statistics, percentage calculations, or formula evaluation"
    is_destructive: bool = False
    category: str = "computation"

    def execute(self, expression: str, **kwargs) -> ToolResult:
        start = time.perf_counter()
        try:
            # Safe evaluation environment
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow,
            })
            # Clean expression
            clean_expr = expression.replace("^", "**").strip()
            result = eval(clean_expr, {"__builtins__": {}}, allowed_names)
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(success=True, output=result, execution_time_ms=round(elapsed, 2))
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(success=False, output=None, error=str(e), execution_time_ms=round(elapsed, 2))
