"""
Rich Interactive CLI for ReflexAgent
"""

from __future__ import annotations
import sys
import os
import typer

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from reflex_agent.core.engine import DualBrainAgent
from reflex_agent.core.schema import AgentMode
from reflex_agent.benchmarks.comparison import run_benchmark_suite

app = typer.Typer(
    name="reflex",
    help="ReflexAgent: Sub-50ms Type-Safe Dual-Brain Agent Framework",
    add_completion=False,
)
console = Console()


@app.command()
def chat(
    mode: str = typer.Option("hybrid", help="Agent mode: 'hybrid', 'pure_reflex', or 'pure_llm'"),
):
    """Start an interactive chat session with live reflex trace."""
    console.print(Panel.fit(
        "[bold cyan]REFLEX-AGENT DUAL-BRAIN INTERACTIVE SHELL[/bold cyan]\n"
        "[dim]System 1 Reflex (Laya / Jev) + System 2 Reasoning (LiteLLM)[/dim]\n"
        "[yellow]Type 'exit' or 'quit' to end session. Type 'telemetry' for statistics.[/yellow]"
    ))

    agent_mode = AgentMode.PURE_REFLEX if mode == "pure_reflex" else AgentMode.HYBRID
    agent = DualBrainAgent(mode=agent_mode)

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]User[/bold green]")
            if not user_input.strip():
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                console.print("[dim]Goodbye![/dim]")
                break
            if user_input.lower() == "telemetry":
                summary = agent.get_telemetry_summary()
                console.print(summary)
                continue

            console.print("[dim]⚡ Evaluating reflex...[/dim]")
            for event in agent.run_stream(user_input):
                color = "cyan" if "System 1" in event.system_level else "yellow"
                if event.event_type == "blocked":
                    console.print(f"[{color}]🔒 {event.message}[/{color}]")
                elif event.event_type == "complete":
                    console.print(f"[dim]⏱ {event.message}[/dim]")
                elif event.event_type == "synthesis":
                    pass
                else:
                    console.print(f"[{color}]▸ {event.message}[/{color}]")

            # Final response
            last_msg = agent.telemetry.traces[-1] if agent.telemetry.traces else None
            # Find assistant response from agent
            console.print(f"\n[bold white]{agent.reasoning.synthesize(user_input, [], '')}[/bold white]")

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


@app.command()
def run(
    query: str = typer.Argument(..., help="Query or task to execute"),
    mode: str = typer.Option("hybrid", help="Agent execution mode"),
):
    """Execute a single query through the Dual-Brain agent."""
    agent_mode = AgentMode.PURE_REFLEX if mode == "pure_reflex" else AgentMode.HYBRID
    agent = DualBrainAgent(mode=agent_mode)

    console.print(f"[bold cyan]Task:[/bold cyan] {query}")
    for event in agent.run_stream(query):
        color = "cyan" if "System 1" in event.system_level else "yellow"
        if event.event_type == "complete":
            console.print(f"[dim]⚡ {event.message}[/dim]")
        elif event.event_type != "synthesis":
            console.print(f"[{color}]▸ {event.message}[/{color}]")

    summary = agent.get_telemetry_summary()
    console.print(Panel(
        f"[green]Latency: {summary.total_latency_ms}ms | Saved: ${summary.dollars_saved_usd} vs pure LLM[/green]",
        title="Execution Complete"
    ))


@app.command()
def bench():
    """Run head-to-head benchmark against OpenClaw and Hermes Agent baselines."""
    run_benchmark_suite()


@app.command()
def guard(
    prompt: str = typer.Argument(..., help="Prompt to test against System 1 Guardrail"),
):
    """Test a prompt against non-autoregressive System 1 Guardrails."""
    agent = DualBrainAgent()
    assessment = agent.guardrail.assess(prompt)

    table = Table(title="[bold red]System 1 Guardrail Assessment[/bold red]")
    table.add_column("Check", style="cyan")
    table.add_column("Result", style="bold")
    table.add_column("Confidence", style="yellow")

    table.add_row("Safe", "[green]YES[/green]" if assessment.is_safe else "[red]NO[/red]", f"{assessment.confidence:.2f}")
    table.add_row("Jailbreak Detected", "[red]YES[/red]" if assessment.is_jailbreak else "[green]NO[/green]", f"{assessment.confidence:.2f}")
    table.add_row("Prompt Injection", "[red]YES[/red]" if assessment.is_prompt_injection else "[green]NO[/green]", f"{assessment.confidence:.2f}")
    table.add_row("Harm Score", f"{assessment.harm_score} ({assessment.harm_level})", f"{assessment.confidence:.2f}")
    table.add_row("Latency", f"{assessment.latency_ms:.2f} ms", "-")

    console.print(table)
    if not assessment.is_safe:
        console.print(f"[bold red]Violation Reason:[/bold red] {assessment.reason}")


@app.command()
def ui(
    host: str = typer.Option("127.0.0.1", help="Host interface"),
    port: int = typer.Option(8000, help="Port to serve dashboard"),
):
    """Launch the Web Dashboard and API server."""
    import uvicorn
    console.print(f"[bold green]Starting ReflexAgent Dashboard at http://{host}:{port}[/bold green]")
    uvicorn.run("reflex_agent.api.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    app()
