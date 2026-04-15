from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic_ai import RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.messages import ToolCallPart
from pydantic_ai.tools import ToolDefinition
from pydantic_ai.toolsets import FunctionToolset

from coding_assistant.deps import AgentDeps


def _path_sandbox(path: str) -> Path:
    return Path("sandbox") / Path(path)


# 1. Implement the read_file tool

# 2. Implement the write_file tool


def search_files(pattern: str) -> list[str]:
    """Search for files matching a glob pattern.

    Parameters
    ----------
    patters : str
        The glob patterns to match files (e.g., "**/*.py", "test_*.py)

    Returns
    -------
    list[str]
        A list of relative file paths matching the pattern.

    """
    sandbox_root = _path_sandbox("")
    matches = sandbox_root.glob(pattern)

    return [str(p.relative_to(sandbox_root)) for p in matches]


# 3. Implement the FileOperations capability. Override the get_toolset() method.
