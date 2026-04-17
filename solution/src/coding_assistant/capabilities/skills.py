from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import frontmatter
from pydantic_ai import RunContext
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
    skill_name: str,
    description: str,
    content: str,
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

    # Make sure the directory exists before writing the skill file. 
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    skill = frontmatter.Post(content)
    skill.metadata["name"] = skill_name
    skill.metadata["description"] = description
    skill.content = content

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(skill))

    return f"Skill written successfully. Content: {skill.content}"


def _build_skills_instructions() -> str:
    files = sorted(Path("skills").glob("*.md"))

    lines = [
        "You can extend your capabilities by using skills.",
        "Use a skill when doing tasks described in the skill.",
        "Use skills to store useful information, procedures, or preferences.",
        "",
        "You have the following skills available:",
    ]

    if not files:
        lines.append("- No skills available yet.")
        return "\n".join(lines)

    for file in files:
        skill = frontmatter.load(str(file))
        name = skill.metadata.get("name", file.stem)
        description = skill.metadata.get("description", "No description provided.")
        lines.append(f"- {name}: {description}")

    return "\n".join(lines)


@dataclass
class Skills(AbstractCapability[Any]):
    def get_instructions(self) -> Callable[[RunContext[Any]], str]:
        def resolve_instructions(ctx: RunContext[Any]) -> str:

            ctx.deps.console.log(
                "Note, the Skills are being re-loaded during run-time ..."
            )

            return _build_skills_instructions()

        return resolve_instructions

    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()
        toolset.add_function(load_skill)
        toolset.add_function(write_skill)
        return toolset
