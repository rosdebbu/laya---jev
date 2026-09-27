"""
Type-Safe Tool Registry with Automatic System 1 Routing Question Synthesis
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from reflex_agent.tools.base import BaseTool, ToolResult
from reflex_agent.core.schema import ChoiceQuestion
from reflex_agent.tools.builtin.calculator import CalculatorTool
from reflex_agent.tools.builtin.file_ops import FileOpsTool
from reflex_agent.tools.builtin.web_search import WebSearchTool
from reflex_agent.tools.builtin.shell_exec import ShellExecTool
from reflex_agent.tools.builtin.memory_store import MemoryStoreTool
from reflex_agent.tools.builtin.mandi_tool import MandiPriceTool
from reflex_agent.tools.builtin.agri_ml import SoilCropRecommendationTool, FertilizerScheduleTool
from reflex_agent.tools.builtin.panchayat_tool import KrishiPanchayatTool
from reflex_agent.tools.builtin.geo_intelligence import GeoIntelligenceTool
from reflex_agent.tools.builtin.live_weather import LiveAgroWeatherTool
from reflex_agent.tools.builtin.gov_schemes import GovtSchemesTool


class ToolRegistry:
    """
    Manages available tools and provides instant System 1 question synthesis.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        self.register(CalculatorTool())
        self.register(FileOpsTool())
        self.register(WebSearchTool())
        self.register(ShellExecTool())
        self.register(MemoryStoreTool())
        self.register(MandiPriceTool())
        self.register(SoilCropRecommendationTool())
        self.register(FertilizerScheduleTool())
        self.register(KrishiPanchayatTool())
        self.register(GeoIntelligenceTool())
        self.register(LiveAgroWeatherTool())
        self.register(GovtSchemesTool())

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[BaseTool]:
        return list(self._tools.values())

    def build_routing_question(self) -> ChoiceQuestion:
        """
        Dynamically synthesizes a System 1 ChoiceQuestion representing all available tools.
        Enables 33ms non-autoregressive tool selection.
        """
        criteria = {}
        for name, tool in self._tools.items():
            criteria[name] = tool.get_routing_criteria()
        criteria["direct_answer"] = "No tool is required; reply directly to the user conversationally"

        return ChoiceQuestion(
            instructions="Which tool or action should be executed next to address `task`?",
            criteria=criteria,
        )

    def execute_tool(self, name: str, **kwargs) -> ToolResult:
        tool = self.get(name)
        if not tool:
            return ToolResult(
                success=False,
                output=None,
                error=f"Tool '{name}' is not registered in ToolRegistry",
            )
        return tool.execute(**kwargs)
