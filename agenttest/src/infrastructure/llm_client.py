"""LLM client abstractions and local fallbacks."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class LLMClient(ABC):
    @abstractmethod
    def call(self, prompt: str, **kwargs) -> str:
        """Call an LLM with a prompt."""

    @abstractmethod
    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        """Analyze user data with an LLM or fallback implementation."""

    def is_available(self) -> bool:
        return False


class MockLLMClient(LLMClient):
    def __init__(self):
        self.call_count = 0

    def call(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        preview = prompt[:200].replace("\n", " ")
        return f"[Mock Response] Received prompt preview: {preview}"

    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        self.call_count += 1
        return f"[Mock Analysis] Analyzed {len(users_data)} users for task: {task}"

    def is_available(self) -> bool:
        return True


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, api_endpoint: str = "https://api.openai.com/v1", model: str = "gpt-4.1-mini"):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.model = model

    def call(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError(
            "OpenAI client integration is not implemented yet. "
            "Wire the provider SDK or HTTP client here before using live calls."
        )

    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        raise NotImplementedError(
            "OpenAI client integration is not implemented yet. "
            "Use the mock provider or add a real provider implementation."
        )

    def is_available(self) -> bool:
        return bool(self.api_key)


class PanguClient(LLMClient):
    def __init__(self, api_key: str, api_endpoint: str = "", model: str = ""):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.model = model

    def call(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError(
            "Pangu client integration is not implemented yet. "
            "Wire the provider SDK or HTTP client here before using live calls."
        )

    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        raise NotImplementedError(
            "Pangu client integration is not implemented yet. "
            "Use the mock provider or add a real provider implementation."
        )

    def is_available(self) -> bool:
        return bool(self.api_key)


def create_llm_client(config: Dict[str, Any]) -> LLMClient:
    provider = (config or {}).get("provider", "mock")
    if provider == "openai":
        return OpenAIClient(
            api_key=config.get("api_key", ""),
            api_endpoint=config.get("api_endpoint", "https://api.openai.com/v1"),
            model=config.get("model", "gpt-4.1-mini"),
        )
    if provider == "pangu":
        return PanguClient(
            api_key=config.get("api_key", ""),
            api_endpoint=config.get("api_endpoint", ""),
            model=config.get("model", ""),
        )
    return MockLLMClient()
