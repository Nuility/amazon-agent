"""配置仓储"""
import os
import json
import yaml
from typing import Dict, Any, Optional
from common.types import SystemConfig
from common.exceptions import ConfigException
from infrastructure.config_validator import ConfigValidator


class ConfigRepository:
    """配置仓储"""
    
    def __init__(self, validator: Optional[ConfigValidator] = None):
        """初始化配置仓储
        
        Args:
            validator: 配置验证器
        """
        self.validator = validator or ConfigValidator()
        self._config_cache: Optional[SystemConfig] = None
    
    def load(self, config_path: str) -> SystemConfig:
        """加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            系统配置
        """
        try:
            if not os.path.exists(config_path):
                raise ConfigException(f"配置文件不存在: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    config_dict = yaml.safe_load(f)
                elif config_path.endswith('.json'):
                    config_dict = json.load(f)
                else:
                    raise ConfigException(f"不支持的配置文件格式: {config_path}")
            
            config_dict = self.apply_env_override(config_dict)
            config = SystemConfig.from_dict(config_dict)
            
            self._config_cache = config
            return config
            
        except ConfigException:
            raise
        except Exception as e:
            raise ConfigException(f"加载配置失败: {str(e)}")
    
    def save(self, config: SystemConfig, config_path: str) -> bool:
        """保存配置
        
        Args:
            config: 系统配置
            config_path: 配置文件路径
            
        Returns:
            保存是否成功
        """
        try:
            config_dict = config.to_dict()
            
            with open(config_path, 'w', encoding='utf-8') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    yaml.dump(config_dict, f, allow_unicode=True, default_flow_style=False)
                elif config_path.endswith('.json'):
                    json.dump(config_dict, f, ensure_ascii=False, indent=2)
                else:
                    raise ConfigException(f"不支持的配置文件格式: {config_path}")
            
            return True
            
        except Exception as e:
            raise ConfigException(f"保存配置失败: {str(e)}")
    
    def get_env_override(self) -> Dict[str, Any]:
        """获取环境变量覆盖配置
        
        Returns:
            环境变量配置字典
        """
        env_config = {}
        
        env_mappings = {
            "AGENTTEST_MAX_BATCH_SIZE": ("max_batch_size", int),
            "AGENTTEST_LOG_LEVEL": ("log_level", str),
            "AGENTTEST_LLM_API_KEY": ("llm_api_config.api_key", str),
            "AGENTTEST_LLM_API_ENDPOINT": ("llm_api_config.api_endpoint", str),
            "AGENTTEST_LLM_MODEL": ("llm_api_config.model", str),
            "AGENTTEST_STORAGE_TYPE": ("data_storage_type", str),
            "AGENTTEST_DATA_FILE_PATH": ("data_file_path", str),
        }
        
        for env_key, (config_key, value_type) in env_mappings.items():
            value = os.environ.get(env_key)
            if value:
                if value_type == int:
                    value = int(value)
                elif value_type == bool:
                    value = value.lower() in ('true', '1', 'yes')
                
                if '.' in config_key:
                    parts = config_key.split('.')
                    if parts[0] not in env_config:
                        env_config[parts[0]] = {}
                    env_config[parts[0]][parts[1]] = value
                else:
                    env_config[config_key] = value
        
        return env_config
    
    def apply_env_override(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """应用环境变量覆盖
        
        Args:
            config_dict: 原始配置字典
            
        Returns:
            合并后的配置字典
        """
        env_config = self.get_env_override()
        
        for key, value in env_config.items():
            if isinstance(value, dict):
                if key not in config_dict:
                    config_dict[key] = {}
                config_dict[key].update(value)
            else:
                config_dict[key] = value
        
        return config_dict
    
    def apply_defaults(self, config: SystemConfig) -> SystemConfig:
        """应用默认值
        
        Args:
            config: 系统配置
            
        Returns:
            应用默认值后的配置
        """
        return config
    
    def get_cached_config(self) -> Optional[SystemConfig]:
        """获取缓存的配置
        
        Returns:
            系统配置
        """
        return self._config_cache
    
    def clear_cache(self):
        """清除配置缓存"""
        self._config_cache = None
