"""大模型API客户端"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class LLMClient(ABC):
    """大模型API客户端抽象基类"""
    
    @abstractmethod
    def call(self, prompt: str, **kwargs) -> str:
        """调用大模型API
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            响应结果
        """
        pass
    
    @abstractmethod
    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        """分析用户数据
        
        Args:
            users_data: 用户数据列表
            task: 分析任务描述
            
        Returns:
            分析结果
        """
        pass
    
    def is_available(self) -> bool:
        """检查API是否可用
        
        Returns:
            是否可用
        """
        return False


class MockLLMClient(LLMClient):
    """模拟大模型客户端（用于测试和降级场景）"""
    
    def __init__(self):
        """初始化模拟客户端"""
        self.call_count = 0
    
    def call(self, prompt: str, **kwargs) -> str:
        """调用模拟API
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            模拟响应
        """
        self.call_count += 1
        return f"[Mock Response] 已收到请求: {prompt[:100]}..."
    
    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        """分析用户数据（模拟）
        
        Args:
            users_data: 用户数据列表
            task: 分析任务描述
            
        Returns:
            模拟分析结果
        """
        self.call_count += 1
        return f"[Mock Analysis] 已分析 {len(users_data)} 个用户，任务: {task}"
    
    def is_available(self) -> bool:
        """检查API是否可用"""
        return True


class OpenAIClient(LLMClient):
    """OpenAI客户端（预留实现）"""
    
    def __init__(self, api_key: str, api_endpoint: str = "https://api.openai.com/v1", model: str = "gpt-3.5-turbo"):
        """初始化OpenAI客户端
        
        Args:
            api_key: API密钥
            api_endpoint: API端点
            model: 模型名称
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.model = model
        self._available = False
    
    def call(self, prompt: str, **kwargs) -> str:
        """调用OpenAI API（预留）
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            响应结果
        """
        raise NotImplementedError("OpenAI客户端未完整实现，请参考使用手册进行配置")
    
    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        """分析用户数据（预留）
        
        Args:
            users_data: 用户数据列表
            task: 分析任务描述
            
        Returns:
            分析结果
        """
        raise NotImplementedError("OpenAI客户端未完整实现，请参考使用手册进行配置")
    
    def is_available(self) -> bool:
        """检查API是否可用"""
        return self._available and bool(self.api_key)


class PanguClient(LLMClient):
    """华为云盘古客户端（预留实现）"""
    
    def __init__(self, api_key: str, api_endpoint: str = "", model: str = ""):
        """初始化盘古客户端
        
        Args:
            api_key: API密钥
            api_endpoint: API端点
            model: 模型名称
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.model = model
        self._available = False
    
    def call(self, prompt: str, **kwargs) -> str:
        """调用盘古API（预留）
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            响应结果
        """
        raise NotImplementedError("盘古客户端未完整实现，请参考使用手册进行配置")
    
    def analyze_users(self, users_data: List[Dict[str, Any]], task: str) -> str:
        """分析用户数据（预留）
        
        Args:
            users_data: 用户数据列表
            task: 分析任务描述
            
        Returns:
            分析结果
        """
        raise NotImplementedError("盘古客户端未完整实现，请参考使用手册进行配置")
    
    def is_available(self) -> bool:
        """检查API是否可用"""
        return self._available and bool(self.api_key)


def create_llm_client(config: Dict[str, Any]) -> LLMClient:
    """创建大模型客户端
    
    Args:
        config: 大模型配置
        
    Returns:
        大模型客户端实例
    """
    provider = config.get("provider", "mock")
    
    if provider == "mock":
        return MockLLMClient()
    elif provider == "openai":
        return OpenAIClient(
            api_key=config.get("api_key", ""),
            api_endpoint=config.get("api_endpoint", "https://api.openai.com/v1"),
            model=config.get("model", "gpt-3.5-turbo")
        )
    elif provider == "pangu":
        return PanguClient(
            api_key=config.get("api_key", ""),
            api_endpoint=config.get("api_endpoint", ""),
            model=config.get("model", "")
        )
    else:
        return MockLLMClient()
