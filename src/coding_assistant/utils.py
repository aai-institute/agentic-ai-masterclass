import os


def get_env(key: str) -> str:
    result = os.getenv(key)
    if result is None:
        raise ValueError(f"Environment variable {key} not set")
    return result
