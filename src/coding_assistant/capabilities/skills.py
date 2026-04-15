from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.toolsets import FunctionToolset


def load_skill(skill_name: str) -> str:
    """Load a skill.

    skill_name : str
        The name of the skill to load.

    Returns
    -------
    str
        The contents of the skill file.

    """
    file_path = f"skills/{skill_name}.md"

    skill = frontmatter.load(file_path)
    return skill.content


@dataclass
class Skills(AbstractCapability[Any]):
    # 1. Override the get_instructions() method.

    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()
        toolset.add_function(load_skill)

        return toolset
