"""日志管理器"""
import logging
import os
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler


class Logger:
    """日志管理器"""
    
    def __init__(
        self,
        name: str = "agenttest",
        log_level: str = "INFO",
        log_file_path: str = "./logs/operation.log",
        log_max_size: int = 10485760,
        log_backup_count: int = 5
    ):
        """初始化日志管理器
        
        Args:
            name: 日志器名称
            log_level: 日志级别
            log_file_path: 日志文件路径
            log_max_size: 日志文件最大大小（字节）
            log_backup_count: 备份文件数量
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            if log_file_path:
                log_dir = os.path.dirname(log_file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                
                file_handler = RotatingFileHandler(
                    log_file_path,
                    maxBytes=log_max_size,
                    backupCount=log_backup_count,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """记录DEBUG日志"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """记录INFO日志"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """记录WARNING日志"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """记录ERROR日志"""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs):
        """记录CRITICAL日志"""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def audit(
        self,
        operation_type: str,
        operator: str,
        target: str,
        result: str,
        error_message: Optional[str] = None
    ):
        """记录审计日志
        
        Args:
            operation_type: 操作类型
            operator: 操作人
            target: 操作目标
            result: 操作结果
            error_message: 错误信息
        """
        message = f"AUDIT | {operation_type} | Operator: {operator} | Target: {target} | Result: {result}"
        if error_message:
            message += f" | Error: {error_message}"
        self.info(message)
    
    def _format_message(self, message: str, **kwargs) -> str:
        """格式化消息"""
        if kwargs:
            extra = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {extra}"
        return message


_global_logger: Optional[Logger] = None


def get_logger() -> Logger:
    """获取全局日志器"""
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger()
    return _global_logger


def init_logger(
    name: str = "agenttest",
    log_level: str = "INFO",
    log_file_path: str = "./logs/operation.log",
    log_max_size: int = 10485760,
    log_backup_count: int = 5
) -> Logger:
    """初始化全局日志器"""
    global _global_logger
    _global_logger = Logger(
        name=name,
        log_level=log_level,
        log_file_path=log_file_path,
        log_max_size=log_max_size,
        log_backup_count=log_backup_count
    )
    return _global_logger
