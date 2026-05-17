"""Logging helpers."""
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    def __init__(
        self,
        name: str = "agenttest",
        log_level: str = "INFO",
        log_file_path: str = "./logs/operation.log",
        log_max_size: int = 10485760,
        log_backup_count: int = 5,
    ):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        self.logger.propagate = False

        if self.logger.handlers:
            return

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file_path:
            try:
                log_dir = os.path.dirname(log_file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)

                file_handler = RotatingFileHandler(
                    log_file_path,
                    maxBytes=log_max_size,
                    backupCount=log_backup_count,
                    encoding="utf-8",
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except OSError as e:
                self.logger.warning(f"File logging unavailable, using console only: {str(e)}")

    def debug(self, message: str, **kwargs):
        self.logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, **kwargs):
        self.logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs):
        self.logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs):
        self.logger.error(self._format_message(message, **kwargs))

    def critical(self, message: str, **kwargs):
        self.logger.critical(self._format_message(message, **kwargs))

    def audit(
        self,
        operation_type: str,
        operator: str,
        target: str,
        result: str,
        error_message: Optional[str] = None,
    ):
        message = f"AUDIT | {operation_type} | Operator: {operator} | Target: {target} | Result: {result}"
        if error_message:
            message += f" | Error: {error_message}"
        self.info(message)

    def _format_message(self, message: str, **kwargs) -> str:
        if kwargs:
            extra = " | ".join([f"{key}={value}" for key, value in kwargs.items()])
            return f"{message} | {extra}"
        return message


_global_logger: Optional[Logger] = None


def get_logger() -> Logger:
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger()
    return _global_logger


def init_logger(
    name: str = "agenttest",
    log_level: str = "INFO",
    log_file_path: str = "./logs/operation.log",
    log_max_size: int = 10485760,
    log_backup_count: int = 5,
) -> Logger:
    global _global_logger
    logger = logging.getLogger(name)
    if logger.handlers:
        logger.handlers.clear()
    _global_logger = Logger(
        name=name,
        log_level=log_level,
        log_file_path=log_file_path,
        log_max_size=log_max_size,
        log_backup_count=log_backup_count,
    )
    return _global_logger
