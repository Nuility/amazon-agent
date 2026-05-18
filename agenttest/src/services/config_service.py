"""Configuration management service."""
import os
from typing import Optional

from common.types import Result, SystemConfig
from repositories.config_repository import ConfigRepository
from infrastructure.config_validator import ConfigValidator
from infrastructure.logger import Logger


class ConfigService:
    def __init__(
        self,
        config_repository: ConfigRepository,
        config_validator: ConfigValidator,
        logger: Logger,
    ):
        self.config_repo = config_repository
        self.validator = config_validator
        self.logger = logger
        self._config: Optional[SystemConfig] = None
        self._config_path: Optional[str] = None

    def load_config(self, config_path: str) -> Result[SystemConfig]:
        try:
            if not os.path.exists(config_path):
                return Result.error(1005, f"Config file does not exist: {config_path}")

            config = self.config_repo.load(config_path)
            errors = self.validator.validate(config.to_dict())
            if errors:
                self.logger.warning(f"Config validation warnings: {'; '.join(errors)}")

            self._config = config
            self._config_path = config_path
            self.logger.info(f"Config loaded from {config_path}")
            return Result.ok(config)
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            return Result.error(1005, str(e))

    def validate_config(self, config: SystemConfig) -> Result[bool]:
        try:
            errors = self.validator.validate(config.to_dict())
            if errors:
                return Result.error(1005, f"Config validation failed: {'; '.join(errors)}")
            return Result.ok(True)
        except Exception as e:
            return Result.error(1005, str(e))

    def reload_config(self) -> Result[SystemConfig]:
        if not self._config_path:
            return Result.error(1005, "No config path has been loaded yet.")

        try:
            self.config_repo.clear_cache()
            result = self.load_config(self._config_path)
            if result.success:
                self.logger.info("Config reloaded successfully")
            return result
        except Exception as e:
            self.logger.error(f"Failed to reload config: {str(e)}")
            return Result.error(1005, str(e))

    def get_config(self) -> SystemConfig:
        if not self._config:
            self._config = SystemConfig()
        return self._config

    def update_config(self, updates: dict) -> Result[SystemConfig]:
        try:
            current = self.get_config().to_dict()
            current.update(updates or {})
            new_config = SystemConfig.from_dict(current)

            validate_result = self.validate_config(new_config)
            if not validate_result.success:
                return Result.error(validate_result.error_code, validate_result.error_message)

            self._config = new_config
            self.logger.info("Config updated in memory")
            return Result.ok(new_config)
        except Exception as e:
            self.logger.error(f"Failed to update config: {str(e)}")
            return Result.error(1005, str(e))
