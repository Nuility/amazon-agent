import yaml
from pathlib import Path
from typing import Any, Dict
import os


class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
    
    def load(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = self._substitute_env_vars(content)
        
        self._config = yaml.safe_load(content)
        return self._config
    
    def _substitute_env_vars(self, content: str) -> str:
        import re
        pattern = r'\$\{([^}]+)\}'
        
        def replace_env_var(match):
            var_name = match.group(1)
            return os.getenv(var_name, match.group(0))
        
        return re.sub(pattern, replace_env_var, content)
    
    def get(self, key: str, default: Any = None) -> Any:
        if not self._config:
            self.load()
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def reload(self) -> Dict[str, Any]:
        return self.load()


config = ConfigLoader()
