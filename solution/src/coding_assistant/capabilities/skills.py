from dataclasses import dataclass
from pathlib import Path
from typing import Any, Annotated
from pydantic import Field

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


def write_skill(
    skill_name: Annotated[
        str,
        Field(
            ...,
            description="The name of the skill to write. Make sure to be expressive as it will be identified by it.",
        ),
    ],
    description: Annotated[
        str,
        Field(
            ...,
            description="A brief description of the skill that's placed at the top of the skill file. Be sure to be expressive as it is used to evaluate the usefulness of the skill.",
        ),
    ],
    content: Annotated[
        str,
        Field(
            ...,
            description="The contents of the skill. Be sure to be expressive and detailed as it describes the skill and how to act on it.",
        ),
    ],
) -> str:
    """Write a new skill.

    You can use this tool to write a new skill to your base in order to store
    useful information, procedures, or code that you can use in the future.

    NOTE: To write new skills, check the SKILL describing how to write skills!

    Parameters
    ----------
    skill_name : str
        The name of the skill to write.
    description : str
        A brief description of the skill.
    content : str
        The contents of the skill.

    Returns
    -------
    str
        The content of the new skill file.
    """
    file_path = f"skills/{skill_name}.md"

    skill = frontmatter.Post(content)
    skill.metadata["name"] = skill_name
    skill.metadata["description"] = description
    skill.content = content

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(skill))

    return f"Skill written successfully. Content: {skill.content}"


@dataclass
class Skills(AbstractCapability[Any]):
    def get_instructions(self) -> str:
        result = (
            "You can extend your capabilities by using skills.\n"
            "Use a skill when doing tasks described in the skill.\n"
            "Use skills to store useful information, procedures, or preferences.\n\n"
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
        toolset.add_function(write_skill)

        return toolset
