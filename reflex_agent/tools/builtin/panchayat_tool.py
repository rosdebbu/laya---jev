"""
Krishi Panchayat Tool for ReflexAgent Dual-Brain System.
Enables System 1 to route complex multi-agent farming trade-offs to the 4-Agent WarRoom.
"""

from typing import Dict, Any, Optional
from reflex_agent.tools.base import BaseTool, ToolResult
from reflex_agent.reasoning.krishi_panchayat import KrishiPanchayatWarRoom

class KrishiPanchayatTool(BaseTool):
    """
    4-Agent Krishi Panchayat Consensus Tool.
    Debates high-stakes trade-offs (e.g. expensive chemical spray vs early harvest vs organic bio-control).
    """

    name: str = "krishi_panchayat"
    description: str = "Multi-agent agricultural consensus debate among Dr. Krishi (Agronomist), Mandi Vyapari (Market Economist), Mitti Mitra (Soil Ecologist), and Gram Sarpanch (Judge). Use when farmer asks whether to spray expensive pesticide, sell early, or make trade-offs between cost and harvest yield."
    category: str = "reasoning"
    is_destructive: bool = False

    def execute(
        self,
        query: str = "Should I spray expensive pesticide or harvest early?",
        crop: str = "Tomato",
        mandi_rate_per_quintal: float = 3800.0,
        acreage: float = 2.0,
        **kwargs
    ) -> ToolResult:
        try:
            warroom = KrishiPanchayatWarRoom()
            consensus = warroom.deliberate(
                query=query,
                crop=crop,
                mandi_rate_per_quintal=mandi_rate_per_quintal,
                acreage=acreage
            )
            return ToolResult(
                success=True,
                output={
                    "query": consensus.query,
                    "crop": consensus.crop,
                    "sarpanch_synthesis_hindi": consensus.sarpanch_synthesis_hindi,
                    "sarpanch_synthesis_english": consensus.sarpanch_synthesis_english,
                    "opinions": [
                        {
                            "agent": op.agent_name,
                            "role": op.role,
                            "verdict": op.verdict,
                            "cost_inr": op.estimated_cost_inr,
                            "urgency": op.action_urgency
                        }
                        for op in consensus.opinions
                    ],
                    "action_items": consensus.action_items,
                    "total_estimated_budget_inr": consensus.total_estimated_budget_inr,
                    "economic_viability_score": consensus.economic_viability_score
                }
            )
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))
