"""
Controlled Shell Execution Tool
Allows executing safe command-line utilities with strict System 1 safety gating.
"""

from __future__ import annotations
import subprocess
import time
from reflex_agent.tools.base import BaseTool, ToolResult


class ShellExecTool(BaseTool):
    name: str = "shell_exec"
    description: str = "Run safe command-line shell utilities (git, npm, python, tests, directory checks)"
    is_destructive: True
    category: str = "system"

    def execute(self, command: str, timeout_seconds: int = 15, **kwargs) -> ToolResult:
        start = time.perf_counter()
        
        # Hard blacklist of catastrophic commands
        lowered = command.lower()
        blocked_keywords = ["rm -rf /", "del /f /s /q c:", "format", "mkfs", ":(){ :|:& };:"]
        for b in blocked_keywords:
            if b in lowered:
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Security Violation: Command contains blocked dangerous token: '{b}'",
                    execution_time_ms=0.0
                )

        try:
            res = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            elapsed = (time.perf_counter() - start) * 1000.0
            output = res.stdout if res.returncode == 0 else (res.stderr or res.stdout)
            return ToolResult(
                success=(res.returncode == 0),
                output=output[:4000],
                error=None if res.returncode == 0 else f"Command failed with exit code {res.returncode}",
                execution_time_ms=round(elapsed, 2)
            )
        except subprocess.TimeoutExpired:
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=False,
                output=None,
                error=f"Command timed out after {timeout_seconds} seconds",
                execution_time_ms=round(elapsed, 2)
            )
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000.0
            return ToolResult(
                success=False,
                output=None,
                error=str(e),
                execution_time_ms=round(elapsed, 2)
            )
