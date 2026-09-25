"""
Example 04: Full Autonomous Dual-Brain Agent Loop
Runs a task through the complete ReflexAgent pipeline:
System 1 Guardrail -> System 1 Routing -> Tool Execution -> System 2 Synthesis.
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reflex_agent.core.engine import DualBrainAgent
from reflex_agent.core.schema import AgentMode

def main():
    print("=" * 70)
    print("🚀 FULL AUTONOMOUS DUAL-BRAIN AGENT LOOP")
    print("=" * 70)

    agent = DualBrainAgent(mode=AgentMode.HYBRID)
    user_query = "Please calculate (450 * 12) + (3800 / 4) and summarize the result."

    print(f"User Query: \"{user_query}\"\n")
    print("Executing agent pipeline:")

    for event in agent.run_stream(user_query):
        print(f"  [{event.system_level}] {event.message}")

    summary = agent.get_telemetry_summary()
    print("\n" + "=" * 70)
    print("TELEMETRY AUDIT REPORT:")
    print(f"  ▸ Total Latency:    {summary.total_latency_ms:.1f} ms")
    print(f"  ▸ System 1 Steps:   {summary.system1_steps} ({summary.system1_percentage}%)")
    print(f"  ▸ Actual Cost:      ${summary.agent_cost_usd:.6f}")
    print(f"  ▸ Pure LLM Cost:    ${summary.hypothetical_llm_cost_usd:.6f}")
    print(f"  ▸ Net Cost Savings: {summary.savings_percentage}% (${summary.dollars_saved_usd:.6f})")
    print(f"  ▸ Speedup Factor:   {summary.speedup_factor}x faster than OpenClaw baseline")
    print("=" * 70)

if __name__ == "__main__":
    main()
