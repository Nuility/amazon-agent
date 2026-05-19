import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import httpx


class LLMClient(ABC):
    @abstractmethod
    async def call(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def analyze_users(self, users_data: List[Dict], task: str) -> str:
        pass
    
    @abstractmethod
    async def stream_call(self, prompt: str, **kwargs):
        pass


class MinimaxClient(LLMClient):
    def __init__(self, api_key: str, endpoint: str, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.endpoint = endpoint
        self.timeout = timeout
        self.max_retries = max_retries
    
    async def call(self, prompt: str, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000)
        }
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(self.endpoint, json=payload, headers=headers)
                    response.raise_for_status()
                    result = response.json()
                    return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        
        return ""
    
    async def analyze_users(self, users_data: List[Dict], task: str) -> str:
        prompt = f"任务: {task}\n\n数据:\n{users_data}"
        return await self.call(prompt)
    
    async def stream_call(self, prompt: str, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000),
            "stream": True
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("POST", self.endpoint, json=payload, headers=headers) as response:
                async for line in response.aiter_lines():
                    if line.strip().startswith("data: "):
                        yield line.strip()[6:]


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4", timeout: int = 30):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.endpoint = "https://api.openai.com/v1/chat/completions"
    
    async def call(self, prompt: str, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000)
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    async def analyze_users(self, users_data: List[Dict], task: str) -> str:
        prompt = f"任务: {task}\n\n数据:\n{users_data}"
        return await self.call(prompt)
    
    async def stream_call(self, prompt: str, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000),
            "stream": True
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("POST", self.endpoint, json=payload, headers=headers) as response:
                async for line in response.aiter_lines():
                    if line.strip().startswith("data: "):
                        yield line.strip()[6:]


class MockLLMClient(LLMClient):
    def __init__(self):
        self.responses = {
            "default": "这是一个模拟响应，用于测试目的。",
            "intent": '{"intent": "query", "confidence": 0.95, "entities": {}}',
            "greeting": "你好！我是Amazon广告助手，很高兴为你服务。",
        }
    
    async def call(self, prompt: str, **kwargs) -> str:
        if "意图" in prompt or "intent" in prompt.lower():
            return self.responses["intent"]
        elif "你好" in prompt or "hello" in prompt.lower():
            return self.responses["greeting"]
        return self.responses["default"]
    
    async def analyze_users(self, users_data: List[Dict], task: str) -> str:
        return f"分析结果: 共{len(users_data)}条数据，任务: {task}"
    
    async def stream_call(self, prompt: str, **kwargs):
        response = await self.call(prompt, **kwargs)
        chunk_size = kwargs.get("chunk_size", 10)
        for i in range(0, len(response), chunk_size):
            yield response[i:i+chunk_size]
            await asyncio.sleep(0.1)
