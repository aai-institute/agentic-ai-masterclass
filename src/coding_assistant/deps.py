from dataclasses import dataclass

from rich.console import Console


@dataclass
class AgentDeps:
    console: Console
