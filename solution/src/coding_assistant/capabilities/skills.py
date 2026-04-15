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
    def get_instructions(self) -> str:
        result = (
            "You can extend your capabilities by using skills.\n"
            "Use a skill when doing tasks described in the skill.\n\n"
            "You have the following skills available:"
        )

        files = Path("skills").glob("*.md")

        for f in files:
            skill = frontmatter.load(str(f))

            name = skill.metadata.get("name")
            description = skill.metadata.get("description")

            result += f"- {name}: {description}"

        return result

    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()
        toolset.add_function(load_skill)

        return toolset
