import asyncio

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich.console import Console
from rich.markdown import Markdown

from coding_assistant.capabilities.file_operations import FileOperations
from coding_assistant.capabilities.reasoning_effort import ReasoningEffort
from coding_assistant.capabilities.skills import Skills
from coding_assistant.deps import AgentDeps
from coding_assistant.utils import get_env

_INSTRUCTIONS = (
    "You are a Python coding agent.\n"
    "* Write clear, correct, and minimal Python code.\n"
    "* Follow the user's instructions exactly, do not add extra features.\n"
    "* Prefer the standard library over external dependencies unless explicitly specified.\n"
    "* Explore the project structure before planning or implementing.\n"
    "* If requirements are unclear, ask a concise clarification question.\n"
    "* Provide a brief summary of your implementation.\n"
    "* Use the available tools.\n"
)


async def run_agent() -> None:
    console = Console()

    provider = OpenAIProvider(
        base_url=get_env("OPENAI_API_BASE"),
        api_key=get_env("OPENAI_API_KEY"),
    )

    model = OpenAIResponsesModel(
        model_name=get_env("MODEL"),
        provider=provider,
    )

    agent = Agent[AgentDeps](
        model=model,
        instructions=_INSTRUCTIONS,
        capabilities=[
            FileOperations(),
            ReasoningEffort(),
            Skills(),
        ],
        deps_type=AgentDeps,
    )

    deps = AgentDeps(console=console)

    message_history: list[ModelMessage] | None = None

    while True:
        user_prompt = console.input(">> ")

        result = await agent.run(
            user_prompt, message_history=message_history, deps=deps
        )
        console.print(Markdown(result.output))

        message_history = result.all_messages()


def main() -> None:
    try:
        asyncio.run(run_agent())
    except EOFError, KeyboardInterrupt:
        pass
