"""异常定义"""
from typing import Optional


class UserManagementException(Exception):
    """用户管理基础异常"""
    
    def __init__(self, message: str, error_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or 1999


class UserNotFoundException(UserManagementException):
    """用户不存在异常"""
    
    def __init__(self, user_id: str):
        super().__init__(f"用户不存在: {user_id}", error_code=1001)
        self.user_id = user_id


class UserAlreadyExistsException(UserManagementException):
    """用户已存在异常"""
    
    def __init__(self, user_id: str):
        super().__init__(f"用户已存在: {user_id}", error_code=1002)
        self.user_id = user_id


class ValidationException(UserManagementException):
    """数据校验失败异常"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, error_code=1003)
        self.field = field


class StorageException(UserManagementException):
    """存储错误异常"""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message, error_code=1004)
        self.original_error = original_error


class ConfigException(UserManagementException):
    """配置错误异常"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message, error_code=1005)
        self.config_key = config_key


class LLMAPIException(UserManagementException):
    """大模型API错误异常"""
    
    def __init__(self, message: str, api_error: Optional[str] = None):
        super().__init__(message, error_code=1006)
        self.api_error = api_error


class BatchLimitExceededException(UserManagementException):
    """批量操作超限异常"""
    
    def __init__(self, batch_size: int, max_limit: int):
        super().__init__(
            f"批量操作数量超限: {batch_size} > {max_limit}",
            error_code=1007
        )
        self.batch_size = batch_size
        self.max_limit = max_limit


class InvalidStatusTransitionException(UserManagementException):
    """无效状态转换异常"""
    
    def __init__(self, current_status: str, new_status: str):
        super().__init__(
            f"无效的状态转换: {current_status} -> {new_status}",
            error_code=1008
        )
        self.current_status = current_status
        self.new_status = new_status
