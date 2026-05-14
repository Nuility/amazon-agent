"""配置管理服务"""
import os
from typing import Optional
from common.types import SystemConfig, Result
from common.exceptions import ConfigException
from repositories.config_repository import ConfigRepository
from infrastructure.config_validator import ConfigValidator
from infrastructure.logger import Logger


class ConfigService:
    """配置管理服务"""
    
    def __init__(
        self,
        config_repository: ConfigRepository,
        config_validator: ConfigValidator,
        logger: Logger
    ):
        """初始化配置管理服务
        
        Args:
            config_repository: 配置仓储
            config_validator: 配置验证器
            logger: 日志器
        """
        self.config_repo = config_repository
        self.validator = config_validator
        self.logger = logger
        self._config: Optional[SystemConfig] = None
        self._config_path: Optional[str] = None
    
    def load_config(self, config_path: str) -> Result[SystemConfig]:
        """加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            加载结果
        """
        try:
            if not os.path.exists(config_path):
                raise ConfigException(f"配置文件不存在: {config_path}")
            
            config = self.config_repo.load(config_path)
            
            config_dict = config.to_dict()
            errors = self.validator.validate(config_dict)
            if errors:
                self.logger.warning(f"配置验证警告: {'; '.join(errors)}")
            
            self._config = config
            self._config_path = config_path
            
            self.logger.info(f"配置加载成功: {config_path}")
            
            return Result.ok(config)
            
        except ConfigException as e:
            self.logger.error(f"配置加载失败: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"配置加载失败: {str(e)}")
            return Result.error(
                error_code=1005,
                message=str(e)
            )
    
    def validate_config(self, config: SystemConfig) -> Result[bool]:
        """验证配置合法性
        
        Args:
            config: 系统配置
            
        Returns:
            验证结果
        """
        try:
            config_dict = config.to_dict()
            errors = self.validator.validate(config_dict)
            
            if errors:
                return Result.error(
                    error_code=1005,
                    message=f"配置验证失败: {'; '.join(errors)}"
                )
            
            return Result.ok(True)
            
        except Exception as e:
            return Result.error(
                error_code=1005,
                message=str(e)
            )
    
    def reload_config(self) -> Result[SystemConfig]:
        """重新加载配置（热更新）
        
        Returns:
            加载结果
        """
        if not self._config_path:
            return Result.error(
                error_code=1005,
                message="未指定配置文件路径"
            )
        
        try:
            self.config_repo.clear_cache()
            result = self.load_config(self._config_path)
            
            if result.success:
                self.logger.info("配置热更新成功")
            
            return result
            
        except Exception as e:
            self.logger.error(f"配置热更新失败: {str(e)}")
            return Result.error(
                error_code=1005,
                message=str(e)
            )
    
    def get_config(self) -> SystemConfig:
        """获取当前配置
        
        Returns:
            系统配置
        """
        if not self._config:
            self._config = SystemConfig()
        return self._config
    
    def update_config(self, updates: dict) -> Result[SystemConfig]:
        """更新配置
        
        Args:
            updates: 配置更新字典
            
        Returns:
            更新后的配置
        """
        try:
            current_dict = self._config.to_dict() if self._config else {}
            current_dict.update(updates)
            
            new_config = SystemConfig.from_dict(current_dict)
            
            validate_result = self.validate_config(new_config)
            if not validate_result.success:
                return Result.error(
                    error_code=validate_result.error_code,
                    message=validate_result.error_message
                )
            
            self._config = new_config
            self.logger.info("配置更新成功")
            
            return Result.ok(new_config)
            
        except Exception as e:
            self.logger.error(f"配置更新失败: {str(e)}")
            return Result.error(
                error_code=1005,
                message=str(e)
            )
