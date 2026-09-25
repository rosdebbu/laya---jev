"""
Unit tests for ReflexAgent Tools and Registry
"""

from reflex_agent.tools.registry import ToolRegistry
from reflex_agent.tools.builtin.calculator import CalculatorTool
from reflex_agent.tools.builtin.memory_store import MemoryStoreTool


def test_calculator_tool():
    calc = CalculatorTool()
    res = calc.execute(expression="25 * 4 + 10")
    assert res.success is True
    assert res.output == 110


def test_memory_store_tool():
    mem = MemoryStoreTool()
    set_res = mem.execute(action="set", key="user_role", value="admin")
    assert set_res.success is True

    get_res = mem.execute(action="get", key="user_role")
    assert get_res.success is True
    assert get_res.output == "admin"


def test_tool_registry_routing_question():
    reg = ToolRegistry()
    q = reg.build_routing_question()
    assert "calculator" in q.criteria
    assert "file_ops" in q.criteria
    assert "direct_answer" in q.criteria
