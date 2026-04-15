import asyncio

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich.console import Console
from rich.markdown import Markdown

from coding_assistant.deps import AgentDeps
from coding_assistant.utils import get_env


async def run_agent() -> None:
    console = Console()

    console.print("Hello, masterclass!")

    # 1. Configure the provider

    # 2. Configure the model

    # 3. Create the agent. Attach the model and instructions

    # 4. Prompt the user for input, run the agent, and print the output
    #    Tip: use console.print(Markdown(result.output))


def main() -> None:
    try:
        asyncio.run(run_agent())
    except EOFError, KeyboardInterrupt:
        pass
