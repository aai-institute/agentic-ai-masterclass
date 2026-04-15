from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic_ai import RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.settings import ModelSettings


@dataclass
class ReasoningEffort(AbstractCapability[Any]):
    def get_model_settings(
        self,
    ) -> Callable[[RunContext[Any]], ModelSettings]:
        def _set_reasoning_effort(ctx: RunContext[Any]) -> ModelSettings:
            user_prompt = str(ctx.prompt)

            if "@low" in user_prompt:
                return ModelSettings(thinking="low")
            if "@high" in user_prompt:
                return ModelSettings(thinking="high")

            return ModelSettings()

        return _set_reasoning_effort
