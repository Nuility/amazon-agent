"""类型定义和数据模型"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Generic, TypeVar
from enum import Enum
from datetime import datetime


class UserStatus(Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class OperationType(Enum):
    """操作类型枚举"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    BATCH_CREATE = "batch_create"
    BATCH_UPDATE = "batch_update"
    BATCH_DELETE = "batch_delete"
    IMPORT = "import"
    EXPORT = "export"
    QUERY = "query"
    ANALYZE = "analyze"


class ErrorCode(Enum):
    """错误码枚举"""
    SUCCESS = 0
    USER_NOT_FOUND = 1001
    USER_ALREADY_EXISTS = 1002
    VALIDATION_ERROR = 1003
    STORAGE_ERROR = 1004
    CONFIG_ERROR = 1005
    LLM_API_ERROR = 1006
    BATCH_LIMIT_EXCEEDED = 1007
    INVALID_STATUS_TRANSITION = 1008
    INVALID_USER_DATA = 1009
    OPERATION_FAILED = 1010
    PERMISSION_DENIED = 1011
    INTERNAL_ERROR = 1999


T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    """统一响应结果"""
    success: bool
    data: Optional[T] = None
    error_code: int = ErrorCode.SUCCESS.value
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: T, metadata: Optional[Dict[str, Any]] = None) -> 'Result[T]':
        """创建成功结果"""
        return cls(
            success=True,
            data=data,
            error_code=ErrorCode.SUCCESS.value,
            metadata=metadata or {}
        )

    @classmethod
    def error(cls, error_code: ErrorCode, message: str, metadata: Optional[Dict[str, Any]] = None) -> 'Result[T]':
        """创建错误结果"""
        return cls(
            success=False,
            error_code=error_code.value,
            error_message=message,
            metadata=metadata or {}
        )


@dataclass
class User:
    """用户实体"""
    user_id: str
    username: str
    email: str
    phone: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE
    attributes: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: int = 0
    updated_at: int = 0
    created_by: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "status": self.status.value,
            "attributes": self.attributes,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """从字典创建"""
        return cls(
            user_id=data.get("user_id", ""),
            username=data.get("username", ""),
            email=data.get("email", ""),
            phone=data.get("phone"),
            status=UserStatus(data.get("status", UserStatus.ACTIVE.value)),
            attributes=data.get("attributes", {}),
            tags=data.get("tags", []),
            created_at=data.get("created_at", 0),
            updated_at=data.get("updated_at", 0),
            created_by=data.get("created_by", "")
        )


@dataclass
class SystemConfig:
    """系统配置"""
    max_batch_size: int = 1000
    enable_llm_integration: bool = False
    llm_api_config: Dict[str, Any] = field(default_factory=dict)
    enable_hot_reload: bool = True
    log_level: str = "INFO"
    log_file_path: str = "./logs/operation.log"
    log_max_size: int = 10485760
    log_backup_count: int = 5
    data_storage_type: str = "file"
    data_file_path: str = "./data/users.json"
    sqlite_db_path: str = "./data/users.db"
    user_id_format: str = "uuid"
    default_user_status: str = "active"
    cache_enabled: bool = True
    cache_ttl: int = 300
    connection_pool_size: int = 10
    sensitive_fields: List[str] = field(default_factory=lambda: ["password", "token", "secret"])
    audit_enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "max_batch_size": self.max_batch_size,
            "enable_llm_integration": self.enable_llm_integration,
            "llm_api_config": self.llm_api_config,
            "enable_hot_reload": self.enable_hot_reload,
            "log_level": self.log_level,
            "log_file_path": self.log_file_path,
            "log_max_size": self.log_max_size,
            "log_backup_count": self.log_backup_count,
            "data_storage_type": self.data_storage_type,
            "data_file_path": self.data_file_path,
            "sqlite_db_path": self.sqlite_db_path,
            "user_id_format": self.user_id_format,
            "default_user_status": self.default_user_status,
            "cache_enabled": self.cache_enabled,
            "cache_ttl": self.cache_ttl,
            "connection_pool_size": self.connection_pool_size,
            "sensitive_fields": self.sensitive_fields,
            "audit_enabled": self.audit_enabled
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemConfig':
        """从字典创建"""
        return cls(
            max_batch_size=data.get("max_batch_size", 1000),
            enable_llm_integration=data.get("enable_llm_integration", False),
            llm_api_config=data.get("llm_api_config", {}),
            enable_hot_reload=data.get("enable_hot_reload", True),
            log_level=data.get("log_level", "INFO"),
            log_file_path=data.get("log_file_path", "./logs/operation.log"),
            log_max_size=data.get("log_max_size", 10485760),
            log_backup_count=data.get("log_backup_count", 5),
            data_storage_type=data.get("data_storage_type", "file"),
            data_file_path=data.get("data_file_path", "./data/users.json"),
            sqlite_db_path=data.get("sqlite_db_path", "./data/users.db"),
            user_id_format=data.get("user_id_format", "uuid"),
            default_user_status=data.get("default_user_status", "active"),
            cache_enabled=data.get("cache_enabled", True),
            cache_ttl=data.get("cache_ttl", 300),
            connection_pool_size=data.get("connection_pool_size", 10),
            sensitive_fields=data.get("sensitive_fields", ["password", "token", "secret"]),
            audit_enabled=data.get("audit_enabled", True)
        )


@dataclass
class OperationLog:
    """操作日志"""
    log_id: str
    operation_type: str
    operator: str
    target_users: List[str]
    operation_params: Dict[str, Any]
    result: str
    error_message: str = ""
    execution_time: int = 0
    timestamp: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "log_id": self.log_id,
            "operation_type": self.operation_type,
            "operator": self.operator,
            "target_users": self.target_users,
            "operation_params": self.operation_params,
            "result": self.result,
            "error_message": self.error_message,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OperationLog':
        """从字典创建"""
        return cls(
            log_id=data.get("log_id", ""),
            operation_type=data.get("operation_type", ""),
            operator=data.get("operator", ""),
            target_users=data.get("target_users", []),
            operation_params=data.get("operation_params", {}),
            result=data.get("result", ""),
            error_message=data.get("error_message", ""),
            execution_time=data.get("execution_time", 0),
            timestamp=data.get("timestamp", 0)
        )


@dataclass
class BatchResult:
    """批量操作结果"""
    total: int
    success_count: int
    failure_count: int
    failures: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """成功率"""
        return self.success_count / self.total if self.total > 0 else 0.0


@dataclass
class Statistics:
    """统计结果"""
    total_users: int
    status_distribution: Dict[str, int]
    tag_distribution: Dict[str, int]
    attributes_distribution: Dict[str, Dict[str, int]]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_users": self.total_users,
            "status_distribution": self.status_distribution,
            "tag_distribution": self.tag_distribution,
            "attributes_distribution": self.attributes_distribution
        }
