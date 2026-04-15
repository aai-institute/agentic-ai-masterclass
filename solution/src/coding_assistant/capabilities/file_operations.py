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


def read_file(path: str) -> str:
    """Read the contents of the file.

    Parameters
    ----------
    path : str
        The relative path to the file.

    Returns
    -------
    str
        The contents of the file.

    """
    return _path_sandbox(path).read_text()


def write_file(path: str, content: str) -> None:
    """Write contents to a file.

    Parameters
    ----------
    path : str
        The relative path to the file.
    content : str
        The contents to be written to the file.

    """
    file_path = _path_sandbox(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)


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


def delete_file(path: str) -> None:
    """Delete a file.

    Parameters
    ----------
    path : str
        The relative path to the file.

    """
    _path_sandbox(path).unlink()


@dataclass
class FileOperations(AbstractCapability[Any]):
    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()

        toolset.add_function(read_file)
        toolset.add_function(write_file)
        toolset.add_function(search_files)
        toolset.add_function(delete_file)

        return toolset

    async def before_tool_execute(
        self,
        ctx: RunContext[AgentDeps],
        *,
        call: ToolCallPart,
        tool_def: ToolDefinition,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        if call.tool_name == "search_files":
            ctx.deps.console.log(f"Searching: {args.get('pattern')}")
        elif call.tool_name == "read_file":
            ctx.deps.console.log(f"Reading: {args.get('path')}")
        elif call.tool_name == "write_file":
            ctx.deps.console.log(f"Writing: {args.get('path')}")

        return args
