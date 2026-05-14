"""配置验证器"""
from typing import Dict, Any, List
from common.exceptions import ConfigException


class ConfigValidator:
    """配置验证器"""
    
    REQUIRED_FIELDS = [
        "max_batch_size",
        "data_storage_type"
    ]
    
    def validate(self, config: Dict[str, Any]) -> List[str]:
        """验证配置合法性
        
        Args:
            config: 配置字典
            
        Returns:
            错误信息列表
        """
        errors = []
        
        errors.extend(self._validate_required_fields(config))
        errors.extend(self._validate_field_types(config))
        errors.extend(self._validate_field_ranges(config))
        errors.extend(self._validate_dependencies(config))
        
        return errors
    
    def _validate_required_fields(self, config: Dict[str, Any]) -> List[str]:
        """验证必填项完整性"""
        errors = []
        for field in self.REQUIRED_FIELDS:
            if field not in config:
                errors.append(f"缺少必填字段: {field}")
        return errors
    
    def _validate_field_types(self, config: Dict[str, Any]) -> List[str]:
        """验证字段类型"""
        errors = []
        
        if "max_batch_size" in config:
            if not isinstance(config["max_batch_size"], int):
                errors.append("max_batch_size 必须为整数")
        
        if "enable_llm_integration" in config:
            if not isinstance(config["enable_llm_integration"], bool):
                errors.append("enable_llm_integration 必须为布尔值")
        
        if "enable_hot_reload" in config:
            if not isinstance(config["enable_hot_reload"], bool):
                errors.append("enable_hot_reload 必须为布尔值")
        
        if "log_level" in config:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if config["log_level"] not in valid_levels:
                errors.append(f"log_level 必须为 {valid_levels} 之一")
        
        if "data_storage_type" in config:
            valid_types = ["file", "sqlite"]
            if config["data_storage_type"] not in valid_types:
                errors.append(f"data_storage_type 必须为 {valid_types} 之一")
        
        return errors
    
    def _validate_field_ranges(self, config: Dict[str, Any]) -> List[str]:
        """验证字段取值范围"""
        errors = []
        
        if "max_batch_size" in config:
            value = config["max_batch_size"]
            if not (1 <= value <= 10000):
                errors.append("max_batch_size 必须在 1-10000 之间")
        
        if "cache_ttl" in config:
            value = config["cache_ttl"]
            if not (0 <= value <= 86400):
                errors.append("cache_ttl 必须在 0-86400 之间")
        
        if "connection_pool_size" in config:
            value = config["connection_pool_size"]
            if not (1 <= value <= 100):
                errors.append("connection_pool_size 必须在 1-100 之间")
        
        return errors
    
    def _validate_dependencies(self, config: Dict[str, Any]) -> List[str]:
        """验证依赖关系"""
        errors = []
        
        if config.get("enable_llm_integration", False):
            llm_config = config.get("llm_api_config", {})
            if not llm_config:
                errors.append("启用大模型集成需要配置 llm_api_config")
            elif not llm_config.get("api_key"):
                errors.append("启用大模型集成需要配置 api_key")
        
        return errors
    
    def validate_strict(self, config: Dict[str, Any]) -> None:
        """严格验证（抛出异常）
        
        Args:
            config: 配置字典
            
        Raises:
            ConfigException: 配置验证失败
        """
        errors = self.validate(config)
        if errors:
            raise ConfigException(
                f"配置验证失败: {'; '.join(errors)}",
                config_key="config"
            )
