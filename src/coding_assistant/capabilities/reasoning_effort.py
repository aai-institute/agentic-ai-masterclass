from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic_ai import RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.settings import ModelSettings


# 1. Implement the ReasoningEffort capability.
#    Override the get_model_settings() method.
